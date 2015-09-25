# twiliosms_wampservice
Twilio SMS service for Crossbar WAMP router

Install the twiliosms_wampservice package in the same Python environment where you have your Crossbar router installed. Then add the below component configuration to config.yaml and start your Crossbar server. Your should see an entry with 'Twilio SMS Sender' showing up in Crossbar server log when it starts.

Then, send SMS messages by making a RPC call to ```services.tele.sms.send``, with two parameters: recipient phone number (in international format), and the SMS message body.

Component configuration follows:

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

Note that you may have to change the router address, port and path settings if your router is not listening at localhost port 8080, at "/ws".
