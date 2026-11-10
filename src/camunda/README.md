# Camunda development environment

Camunda 8.8.44 runs the process engine, Tasklist and Operate in one container.
Elasticsearch 8.17.10 is its secondary storage. The marketplace PostgreSQL database
is separate. Connectors, Optimize, Keycloak and a hosted model editor are not included.

The configuration is adapted from the official Camunda 8.8 lightweight distribution:
https://github.com/camunda/camunda-distributions/tree/80ebf43/docker-compose/versions/camunda-8.8

From the repository root, with Docker running:

```sh
docker compose up -d camunda-deploy
docker compose logs -f camunda-deploy
```

This starts Camunda, Elasticsearch and a one-off deployment container. A successful
deployment exits with code 0; failures exit with code 1 and explain the problem in the logs. On the first run, downloading the images
and initializing storage can take several minutes.

Tasklist: http://localhost:8088/tasklist
Operate: http://localhost:8088/operate
Username: demo
Password: demo

These are development settings. Browser access uses the demo account; API authentication
and authorization are disabled. Published ports are bound to the host loopback
interface. Elasticsearch has no published host ports.

The REST API is http://localhost:8088/v2, and the gRPC endpoint is localhost:26500.
Containers on the Compose network use http://camunda:8080/v2 and camunda:26500.
The frontend keeps its separate port 8080.

## Processes and forms

The `camunda-deploy` service waits for Camunda to be healthy, then uploads the BPMN
files listed in `deployments.txt` and every `.form` file under `form_files` (or `bpmn_files`) in one
atomic request. The current selection is the newer F1 model. The strategic
model is excluded deliberately; add further executable models to the list when ready.

Export Camunda forms from Web Modeler into `form_files`. Form IDs must match
the references in BPMN. Deployment stops with an explanation if a referenced form
is missing. Camunda validates the BPMN and returns any remaining deployment errors.
The files are not modified by deployment.

`docker compose up -d` also includes this deployment service. Starting only `camunda`
or running `docker compose restart camunda` does not run deployment. To redeploy
changed files explicitly:

```sh
docker compose run --rm camunda-deploy
```

## Run F1

1. In Tasklist, open **Processes** and start **New Product Submission, Validation and Publication (f1)**.
2. Fill in **Enter Product Details** with a [demo producer ID](../database/README.md#demo-producer-for-f1) and a new submission key.
3. If **Correct Product Details** comes up, fix the fields it flags and resubmit with the same key.

## Stop and inspect

```sh
docker compose ps camunda elasticsearch
docker compose logs --tail=100 camunda elasticsearch
docker compose stop camunda elasticsearch
```

Named volumes retain process/task data and Elasticsearch indexes across restarts.
Do not use `docker compose down -v` unless deleting project database and
workflow data. Editing initialization users does not reset existing persisted users.
