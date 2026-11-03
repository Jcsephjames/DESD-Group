verification.py

Job type: Not registered in the runner yet; the BPMN expects verify-certificate.

Workflow: Organic claim -> certification service request -> certificate decision.

The current helper POSTs certificate_id to CERTIFICATION_SERVICE_URL and returns its JSON response. It does not complete Camunda jobs. A service contract, runner adapter and separate handling for rejection versus service unavailability are still needed.

The shared runner owns polling and technical failure handling. Only handlers in
runner.py HANDLERS are active. Do not start a second standalone polling process
when demonstrating the shared runner.
