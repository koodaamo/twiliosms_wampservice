# twiliosms_wampservice
Twilio SMS service for Crossbar WAMP router

Install the twiliosms_wampservice package in the same Python environment where you have your Crossbar router installed. Then add the below component configuration to config.yaml and start your Crossbar server. Your should see an entry with 'Twilio SMS Sender' showing up in Crossbar server log when it starts.

Then, send SMS messages by making a RPC call to ```services.tele.sms.send``, with two parameters: recipient phone number (in international format), and the SMS message body.

SMS sender component configuration follows:

```yaml
- classname: twiliosms_wampservice.SMSSender
  id: Twilio SMS Sender
  realm: realm1
  extra:
    twilio-account: "" <--- replace "" with your account id
    twilio-token: "" <--- replace "" with your account token
    twilio-number: "" <--- replace "" with your ('sending') Twilio SMS number
  transport:
    endpoint: {host: 127.0.0.1, port: 8080, type: tcp}
    type: websocket
    url: ws://127.0.0.1:8080/ws
  type: class
```

(Note that you may have to change the router address, port and path settings in the above configuration, if your router is not listening at localhost port 8080, at "/ws".)

For the SMS receiver, likewise add the following configuration:

```yaml
- classname: twiliosms_wampservice.SMSReceiver
  id: Twilio SMS Receiver
  realm: realm1
  extra:
    twilio-token: "" <--- replace "" with your account token
    receiver-address: "" <--- replace "" with a valid local address to bind to 
    receiver-port: "" <--- replace "" with a valid port number to listen at
    receiver-path: "" <--- replace "" with the URL path the receiver should accept POST requests at
  transport:
    endpoint: {host: 127.0.0.1, port: 8080, type: tcp}
    type: websocket
    url: ws://127.0.0.1:8080/ws
  type: class
```

Note that the receiver will perform request validity checking according to https://www.twilio.com/docs/security.
