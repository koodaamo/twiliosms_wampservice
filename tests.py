import unittest
from twiliosms_wampservice import app, SMSSender

class Config(object):
   extra = {"twilio-account":"", "twilio-token":"", "twilio-number":""}

class TestInstantiation(unittest.TestCase):

   def test_sender_instantiation(self):
      s = SMSSender(Config())
