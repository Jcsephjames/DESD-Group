# Test F1 certificate checks

For our demo, use `BIO-123` to pass or `ABC-123` to trigger a correction.
To test an outage, run `docker compose stop certification` before submitting an
organic product. Once it reaches pending verification, run
`docker compose start certification` and send the message below with the
original submission key.

```sh
curl -fsS http://localhost:8088/v2/messages/publication \
  -H 'Content-Type: application/json' \
  -d '{"name":"certification-service-restored","correlationKey":"YOUR_SUBMISSION_KEY","timeToLive":60000}'
```
