from .twiliosms import SMSSender


def app(config):
    ##
    # This component factory creates instances of the
    # application component to run.
    ##
    # The function will get called either during development
    # using ApplicationRunner, or as  a plugin running
    # hosted in a WAMPlet container such as a Crossbar.io worker.
    ##
    if config:
        raise Exception("SMSSENDER CALLED")
        return SMSSender(config)
    else:
        # if no config given, return a description of this WAMPlet ..
        return {'label': 'Twilio SMS Service WAMPlet',
                'description': 'WAMP application component of Twlilio SMS WAMPlet'}
