# Blue Bite Assessment

## Introduction

Imagine a system which needs to serve payloads for millions of different smart objects. Each object can hold multiple data parameters describing the object it's attached to. The set of parameters is not consistent across all objects because each object can be attached to a different item (e.g. a shoe, a soccer ball, or a bag). Imagine we have multiple batch operations which are sending us JSON payloads containing existing objects or new objects that need to be created.

## Data Constraints

There is a JSON Schema that describes the format of incoming payloads. [It can be found  here](files/schema.json). You may use it to validate incoming payloads

Each object record will be part of an array and will look something like this
```json
{
  "object_id": "0fadf66d045648bfa880d7d07af203bb",
  "data": [
    {
      "key": "type",
      "value": "shoe"
    },
    {
      "key": "color",
      "value": "blue"
    },
    {
      "key": "demo",
      "value": true
    },
    {
      "key": "cost",
      "value": 20.34
    }
  ]
}
```

Example payloads can be found in [files directory](files)

## Requirements

### Part 1

* The application should accept JSON payloads via a route
    * When the application receives a new payload it must be validated (reference schema), parsed and (if the data is correct) stored in the database
    * The application must be able to handle validation errors. The format of the errors is your choice so long as it is consistent and adheres to HTTP protocol standards.

### Part 2
* The application must offer a way to query a list of objects based on filters.
    * Must filter on object_id, key, and/or value


## Submission

Upon completion of the assessment, please email your point of contact at Blue Bite a link to the repository.


## Local Setup

Your system needs to be able to:
 - Run `docker-compose` (you will need an up to date version of `docker` installed)
 - Run a `bash` script

Everything is dockerized so as long as you are running an up to date version of docker
then everything will work. The automated spin up maps the app port to `8000` for
convenience.

### Basic Spin-up

Run `./scripts/run-local`

This will spin up a `postgres` container and an `app` container that is running a bare
Django app on a hot-loaded debug server. After spin-up, the command will run the database
migrations. This does not seed any users or super users.
