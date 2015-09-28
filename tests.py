import unittest, hmac, base64, hashlib, urllib
from twilio.util import RequestValidator
from klein.test.test_resource import requestMock
from twiliosms_wampservice import SMSSender, SMSReceiver

test_account = "AAA000"
test_token = "123ABC"
test_sender = "+35812345678"
test_recipient = "+3589876543"
test_message = "Hello World!"
test_host = "127.0.0.1"
test_port = 9090
test_path = "/services/tele/sms/new"
test_url = "%s:%i%s" % (test_host, test_port, test_path)
test_form = {
   "From": test_sender,
   "To": test_recipient,
   "Body": test_message
}

class Config(object):
   def __init__(self, extra):
      self.extra = extra


def generate_signature(url, form, token):
   _sorted = sorted(form)
   formstring = ''.join([k + form[k] for  k in _sorted])
   hash = hmac.new(token, url+formstring, hashlib.sha1).digest()
   return base64.b64encode(hash)


class TestInstantiation(unittest.TestCase):

   def test_sender_instantiation(self):
      extra = {
         "twilio-account": test_account,
         "twilio-token": test_token,
         "twilio-number": test_sender
      }
      s = SMSSender(Config(extra))

   def test_receiver_instantiation(self):
      extra = {"twilio-token": test_token, "twilio-receiver": test_url}
      s = SMSReceiver(Config(extra))


class TestTwilio(unittest.TestCase):

   def test_signature_generator(self):
      signature = generate_signature(test_url, test_form, test_token)
      validator = RequestValidator(test_token)
      self.assertTrue(validator.validate(test_url, test_form, signature))

   def test_verification(self):
      extra = {"twilio-token": test_token, "twilio-receiver": test_url}
      s = SMSReceiver(Config(extra))
      signature = generate_signature(test_url, test_form, test_token)
      headers = {"X-Twilio-Signature": [signature]}
      r = requestMock(test_path, method="POST", host=test_host,
                     port=test_port, body=urllib.urlencode(test_form), headers=headers)
      r.args = test_form
      self.assertTrue(s.validSignature(r))
