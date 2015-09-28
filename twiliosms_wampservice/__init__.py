from .twiliosms import SMSSender, SMSReceiver


def sender(config):
    ##
    # component factory to creates instances of SMS sender application component to run
    # called either during development using ApplicationRunner, or as  a plugin running
    # hosted in a WAMPlet container such as a Crossbar.io worker.
    ##
    if config:
        return SMSSender(config)
    else:
        # if no config given, return a description of this WAMPlet ..
        return {'label': 'Twilio SMS sender service WAMPlet',
                'description': 'WAMP application component of Twlilio SMS WAMPlet'}


def receiver(config):
    ##
    # component factory to creates instances of SMS receiver application component to run
    # called either during development using ApplicationRunner, or as  a plugin running
    # hosted in a WAMPlet container such as a Crossbar.io worker.
    ##
    if config:
        return SMSReceiver(config)
    else:
        # if no config given, return a description of this WAMPlet ..
        return {'label': 'Twilio SMS receiver service WAMPlet',
                'description': 'WAMP application component of Twlilio SMS WAMPlet'}
