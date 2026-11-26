# SMS Automation

Send SMS via Twilio, daily scheduled + custom menu.

 Requirements

```bash
pip install twilio schedule
```

 Setup - never hardcode secrets

```bash
$env:TWILIO_ACCOUNT_SID='AC...'; $env:TWILIO_AUTH_TOKEN='...'; $env:TWILIO_FROM='+15005550006'; $env:SMS_TO='+919999999999'; $env:SMS_TIME='08:00'
```

 Run

```bash
python index.py
```
