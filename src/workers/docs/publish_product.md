publish_product.py

Job type: Not registered in the runner yet; the BPMN expects publish-product.

Workflow: Successful validation/certification -> Save and Publish Product.

The helper inserts product fields using a caller-provided SQL connection and commits or rolls back. It still needs alignment with the required schema fields, retry-safe persistence and a listing-published message. It is not a complete publication worker yet.

The shared runner owns polling and technical failure handling. Only handlers in
runner.py HANDLERS are active. Do not start a second standalone polling process
when demonstrating the shared runner.
