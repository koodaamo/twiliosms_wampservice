import sys
from os import environ
import datetime

from twisted.logger import Logger, globalLogPublisher
from twisted.logger import textFileLogObserver
from twisted.internet.defer import inlineCallbacks
import treq
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

SMS_PROCEDURE = u"services.tele.sms.send"


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

