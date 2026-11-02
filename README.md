# DESD-Group

Group Members - Faris Drury
              - Billy Manzi
              - Joseph Moore
              - Leyla 
            

Chosen Use Case - Producer Product Listing and Inventory Management

# Folder Layout 
/docs/analysis/ = business and stankholder analysis and functional requirments 
/docs/planning/ = backlogs and plans
/docs/assessment/ = all assessment information
/Models/ = BPMN Models and i* SD and SR models
/Readme = overveiw of this task and groups work and how to run everything 

# Learning simulation

## Camunda and Tasklist

See [Camunda setup](src/camunda/README.md) to start the lightweight Docker environment.
Tasklist runs at http://localhost:8088/tasklist with the development login `demo` / `demo`.
Processes and forms must be deployed before tasks appear.

## PostgreSQL database mock-up

PostgreSQL and the Python workers are configured in `docker-compose.yml`.
See [database setup](src/database/README.md) and [workers setup](src/workers/README.md)
for startup instructions. The workers image installs its own dependencies; a host
`.venv` is not required to run the containers.

## Run the learning simulation

Run `python3 simulation.py` from this folder. Choose a scenario and press Enter
to follow each step. It uses no packages, Camunda installation, server, or database.
It only demonstrates the flow; it does not connect to or replace Camunda.

The Docker implementation uses Camunda for process control, Forms for user input,
and Python workers for automated tasks. The use-case sheet permits
an external or simulated certificate verification service.
