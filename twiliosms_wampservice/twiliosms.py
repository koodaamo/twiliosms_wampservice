import sys
import datetime
import cgi
import os

from twisted.web.server import Site
from twisted.logger import Logger, globalLogPublisher
from twisted.logger import textFileLogObserver
from twisted.internet.defer import inlineCallbacks, succeed, fail, returnValue
from twisted.internet import reactor
import treq
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from klein import route, Klein
from twilio.util import RequestValidator

SMS_PROCEDURE = u"services.tele.sms.send"
SMS_EVENT = u"services.tele.sms.new"

class SMSReceiver(ApplicationSession):

   webapp = Klein()
   logger = Logger()

   def __init__(self, config):
      ApplicationSession.__init__(self)
      self.t_token = config.extra["twilio-token"]
      self.t_receiver = config.extra["twilio-receiver"]
      self.t_validator = RequestValidator(self.t_token)
      self.logger.info("receiving SMS at %s" % '/'+ SMS_EVENT.replace('.','/'))

   def onConnect(self):
      self.join("realm1")
      reactor.listenTCP(9090, Site(self.webapp.resource()))

   def validSignature(self, request):
      signature = request.getHeader("X-Twilio-Signature")
      if not signature:
         return False
      return self.t_validator.validate(self.t_receiver, request.args, signature)

   @webapp.route('/'+ SMS_EVENT.replace('.','/'), methods=['POST'])
   @inlineCallbacks
   def receive(self, request):
      "publish incoming new SMS as (sender, recipient, message)"
      if self.validSignature(request):
         form = request.args
         msg = (form["sender"], form["recipient"], form["message"])
         yield self.session.publish(SMS_EVENT, msg)
         returnValue(succeed(None))
      else:
         request.setResponseCode(401)
         signature = request.getHeader("X-Twilio-Signature") or "(no signature)"
         returnValue("Missing or invalid signature: %s" % signature)


class SMSSender(ApplicationSession):

   logger = Logger()

   def __init__(self, config):
      ApplicationSession.__init__(self)
      self.t_account = config.extra["twilio-account"]
      self.t_token = config.extra["twilio-token"]
      self.t_number = config.extra["twilio-number"]
      urltmpl = "https://api.twilio.com/2010-04-01/Accounts/%s/Messages"
      self.t_url = (urltmpl % self.t_account).encode("utf-8")

   def onConnect(self):
      self.join("realm1")

   def onOK(self, response, recipient, message):
      if response.code==201:
         self.logger.debug("queued message '%s' for delivery to %s" % (message, recipient))
      else:
         errmsg = "queuing of message '%s' to %s failed: %i %s"
         self.logger.debug(errmsg % (message, recipient, response.code, response.phrase))

   def onFAIL(self, failure, recipient, message):
      errmsg = "queuing of message '%s' to %s failed: %s"
      self.logger.debug(errmsg % (message, recipient, str(failure)))

   @inlineCallbacks
   def onJoin(self, details):
      self.logger.info("SMS sender session opened with router")

      def sendSMS(recipient, message):
         t_form = {"From":self.t_number, "To":recipient, "Body":message}
         d = treq.post(self.t_url, auth=(self.t_account, self.t_token), data=t_form)
         d.addCallback(self.onOK, recipient, message)
         d.addErrback(self.onFAIL, recipient, message)
         return "OK"

      try:
         yield self.register(sendSMS, SMS_PROCEDURE)
      except Exception as e:
         self.logger.debug("failed to register procedure with router: {}".format(e))
      else:
         self.logger.debug("procedure '%s' registered with router" % SMS_PROCEDURE)

