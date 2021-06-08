# Noyo Coding Challenge

- [Noyo Coding Challenge](#noyo-coding-challenge)
  - [Logistics](#logistics)
    - [Implementation Options](#implementation-options)
    - [Submission Options](#submission-options)
    - [Support](#support)
  - [Address Segment API](#address-segment-api)
    - [Overview](#overview)
    - [The Existing Codebase](#the-existing-codebase)
    - [The Challenge: Address Segment Endpoint](#the-challenge-address-segment-endpoint)
    - [Live Extensions](#live-extensions)
  - [Instructions For Running](#instructions-for-running)
    - [Building the App](#building-the-app)
    - [Running the App](#running-the-app)
    - [Running the Tests](#running-the-tests)
    - [Seeding the Database](#seeding-the-database)
    - [Connecting to the Database](#connecting-to-the-database)
    - [Formatting your Code](#formatting-your-code)
    - [Starting Over](#starting-over)

## Logistics

### Implementation Options

You have two options for completing this exercise:
1. **Complete it prior to your interview:** In the live session, you'll review your solution with the interviewer and work through one or more of the [Live Extensions](#live-extensions). If you choose this option we ask that you spend **no more than 1-2 hours on it**, if you are unable to complete within the time recommendation please find a stopping point and you can work through the remainder during the live interview.

2. **Complete it during your interview:** We ask that you spend **20-30 minutes** familiarizing yourself with the exercise and ensuring you can start the server on your machine prior to the live interview. During the interview you will pair with the interviewer to complete the exercise and one or more of the [Live Extension](#live-extensions).

### Submission Options

You have two options for completing the exercise, choose the one that you are most comfortable with:

1. Zip up your code and email it to coding-challenge@noyo.com 
  
2. Commit your code to a public Github repository and share the link to the code in an email to coding-challenge@noyo.com

**Note: Please do not fork this repository or open a pull request with your submission against this repository.**

### Support 

If you have any technical issues or questions about the instructions below please email coding-challenge@noyo.com and we will get back to you as soon as possible.

## Address Segment API

### Overview

Time-based data is an important concept here at Noyo, frequently we need to understand not only what the current state of a model is, but also what it looked like at a point in the past (and sometimes the future). The purpose of this application is to store records of people and to track their address over time.


### The Existing Codebase

We have provided you with an existing API application built in Flask. We've gone ahead and implemented following:

* Database tables and models for both `Person` and `AddressSegment`
* API Endpoints to manage the `Person` model
* A unit test suite to test the `/person` endpoints and a subset of the `/address` endpoints

You can find [instructions for running](#instructions-for-running) the server, the test suite, and other information in this document.

### The Challenge: Address Segment Endpoint

For this exercise, you'll add functionality to the `PUT /api/persons/<person_id>/address` endpoint, which creates an `AddressSegment` for the `Person` with the specified ID.

To begin you will need to [start the server](#running-the-app) and create some `Person` records either by making calls to the server or running the [seed](#seeding-the-database) helper we've provided.

After you've created at least one `Person`, plug their `id` into the following `curl` command (or construct an API call using the tool of your choice).  

```bash
curl -X PUT \
  http://localhost:3000/api/persons/<person_id>/address \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-01-01",
    "street_one": "123 Main Street",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94613"
  }'
```

Making the previous API call will create a single `AddressSegment` record for the `Person` with a `start_date` of `2021-01-01` and an `end_date` of `null`. In our data model this means that the person's address was `123 Main Street San Francisco, CA 94613` starting on `2021-01-01` and will remain that indefinitely. The following diagram is a visual representation that:

![Diagram of a single address segment starting at 2021-01-01 and extending indefinitely](/docs/address_one_segment.png)

Now we make another API call that updates the Person's address to `1 California Street San Francisco, CA 94111` starting on `2021-06-15`. **In the application's current state this should result in the server raising a `NotImplementedError`**.

```bash
curl -X PUT \
  http://localhost:3000/api/persons/<person_id>/address \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-06-15",
    "street_one": "1 California Street",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94111"
  }'
```

Your challenge is to update the [code on this endpoint](/service/api/addresses.py#L68) to handle the creation of subsequent address segments. In this example, after the API call has been issued we would expect the segments of the address to look like the following diagram:

![Diagram of an address segment starting at 2021-01-01 and ending on 2021-06-15, followed by a second segment extending indefinitely](/docs/address_two_segment.png)

In order to assist with implementing this endpoint we have provided a [failing test case](/tests/api/test_addresses.py#L99) that matches the example laid out above.

### Live Extensions

**Note: During your live coding interview, we will ask you to implement one or more of the following extensions to the code. You should not implement any of these extensions prior to the interview. You are welcome to look at them if you'd like, but we don't want you to spend any additional time implementing them beforehand.**

* [Extension One: `start_date` Validation](/docs/extension_one.md)
* [Extension Two: Get Address by Date](/docs/extension_two.md)
* [Extension Three: Merge Contiguous Identical Address Segments](/docs/extension_three.md)


## Instructions For Running

Here at Noyo we rely on [Docker Compose](https://docs.docker.com/compose/) to ensure portability of our applications and let developers spend more time developing and less time configuring their local environment. We've provided a `docker-compose.yml` that installs all the appropriate dependencies and creates a database that the application can connect to.

*Note: Docker Compose is now bundled along with Docker for Desktop on both Mac and Windows. You may use the syntax `docker compose` rather than `docker-compose` for the following instructions.*

### Building the App

You can build the server and database containers using the following command:

```bash
docker-compose build
```

### Running the App

You can start the server and database using the following command:

```bash
docker-compose up
```

This will start up the [Python Flask](https://flask.palletsprojects.com/en/1.1.x/) server on `localhost:3000` and a PostgreSQL instance on `localhost:5432`.

Flask starts up in debug mode, meaning whenever you save a file it will restart the server with your changes.

### Running the Tests

We have provided a test suite that uses [pytest](https://docs.pytest.org/en/stable/). You can run the test suite using the following:

```bash
docker-compose exec service pytest .
```

*Note: To keep things simple the tests use the same database as the local server. This means when you run tests the database will be cleared of all data.*

### Seeding the Database

To make it easier to work with the API, we've provided a simple Python script that you can run to create 5 random `person` entries in the database. You can run the seed using the following:

```bash
docker-compose exec service python seed.py
```

*Note: You can only run the seed after you have started the server using `docker-compose up`*

### Connecting to the Database

The schema for the database is created for you when you start up the container by executing the contents of [`schema.sql`](/schema.sql). If you would like to connect to the application's database, you can do so using the PostgreSQL client of your choice and using the following configuration:

|Parameter|Value|
|-|-|
|Host|127.0.0.1|
|Port|5432
|Database|coding_challenge|
|Username|noyo|
|Password|noyo|

### Formatting your Code

Here at Noyo, we use [Black](https://github.com/psf/black) to handle the formatting of our code. This enables to spend less time during code reviews worrying about spacing and indents and more time focusing on the content. If you would like to format your code using Black you can run the following command:

```bash
docker-compose exec service black .
```

### Starting Over

If you get your database or local server into a weird state you can start anew by running:

```bash
docker-compose down --remove-orphans --volumes
```

Then go back to [Running the App](#running-the-app) and start over.
