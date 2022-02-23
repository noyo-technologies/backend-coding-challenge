
# Table of Contents
- [Table of Contents](#table-of-contents)
  - [TLDR;](#tldr)
- [Noyo Coding Challenge! (Introduction)](#noyo-coding-challenge-introduction)
  - [Problem 1. Implement Feature (~ 2 Hours)](#problem-1-implement-feature--2-hours)
    - [Business Rules](#business-rules)
- [What we are evaluating](#what-we-are-evaluating)
- [What we are not evaluating](#what-we-are-not-evaluating)
- [Cheat Sheet](#cheat-sheet)
- [Submission Options](#submission-options)
  - [Support](#support)
  - [Live Extensions](#live-extensions)
  - [Instructions For Running](#instructions-for-running)
    - [Building the App](#building-the-app)
    - [Running the App](#running-the-app)
    - [Running the Tests](#running-the-tests)
    - [Seeding the Database](#seeding-the-database)
    - [Connecting to the database](#connecting-to-the-database)
    - [Formatting your Code](#formatting-your-code)
    - [Debugging](#debugging)
    - [Starting Over](#starting-over)
- [Thanks!](#thanks)

## TLDR;
1. You need docker, install it
2. Run this... and 12 test pass, no warnings
      ```sh
      docker compose build # build some stuff
      docker compose up -d && sleep 5 # start the server and wait
      docker-compose exec service python seed.py # seed the db 
      docker compose exec service pytest . # run some tests
      ```
3. Do [Take Home Problem 1](#problem-1-implement-feature--2-hours)
4. If you need to start over
   ```sh
   docker-compose down --remove-orphans --volumes # nuke all the things
   ```
5. Look at the [Live Extensions](#live-extensions), if you want, but dont do them.

# Noyo Coding Challenge! (Introduction)

Within this repository is a python application that implements v1.0 of a fictitious product specification. The story goes that Noyo is partnering with innovative insurance companies offering a new type of coverage called "traveling salesperson insurance.". This offering gives a company's employees unique benefits when they are on the road. It considers various aspects of their travel and has some very complex plan eligibility rules. When a salesman is working out of a home office, there could be gaps in their coverage timeline. 

This code was deployed to production as is, but is incomplete, the original engineer was on a tight timeline, and did his best; it is possible that there are bugs in the code in addition to incomplete or incorrect tests. 

**Note**  
For this challenge there are **no intentionally** included bugs that you have to seek out or find. The incomplete tests however, are intentional and we encourage you to add more. If you find something that you think is a bug, lets talk about it during your onsite!


**Part 1 (Take home - Completed before the interview) ~ 2 Hours**  
Development has halted and product is incomplete!  
1. Complete development as outlined in the challenge. 

**Part 2 (Onsite - Pair programming session) ~ 90 Minutes**  
An engineer has joined your team, show them the ropes!  
1. Discuss the take-home portion in Part 1
2. Live code implementation of additional features.

## Problem 1. Implement Feature (~ 2 Hours)

For this exercise, you'll add functionality to the `PUT /api/persons/<person_id>/segment` endpoint, which creates a `Segment` for the `Person` with the specified ID.

To begin, you will need to [start the server](#running-the-app) and create some `Person` records either by making calls to the server or running the [seed](#seeding-the-database) helper we've provided.

After you've created at least one `Person`, plug their `id` into the following `curl` command (or construct an API call using the tool of your choice).

```bash
curl -X PUT 
  http://localhost:3000/api/persons/<person_id>/segment \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-01-01",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94613"
}'
```

The previous API does nothing but should create a single `Segment` record for the `Person` with a `start_date` of `2021-01-01` and an `end_date` of `null`. In our data model, this means that the person's location was `San Francisco, CA 94613` starting on `2021-01-01` and will remain that indefinitely. The following diagram is a visual representation that:

![diagram of a single address segment starting at 2021-01-01 and extending indefinitely](/docs/address_one_segment.png)

Making another API call that updates the person's address to `San Francisco, CA 94911` starting on `2021-06-15`. Should add this new segment to the person's existing segment list.

```bash
curl -X PUT 
  http://localhost:3000/api/persons/<person_id>/segment \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-06-15",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94911"
  }'
```
![diagram of an address segment starting at 2021-01-01 and ending on 2021-06-15, followed by a second segment extending indefinitely](/docs/address_two_segment.png)

Your challenge is to update the [code on this endpoint](/service/api/segments.py#L51) to handle the creation of address segments. 

### Business Rules
1. You can only add segments to the end.
    1. That is, adding a segment whose start date is before ANY existing start date should result in a 422.
2. A segments end date of None should be treated as indefinitely in the future.
3. A new segment that we are adding can have an end date.
4. Update the end_date of an existing segment to the start_date of the new segment.
    1. If the existing segments end_date is before the new segment's start_date then no update to the existing segment is required... Meaning, you can't have overlapping segments, but there can be gaps between segments.
5. The endpoint should implement http PUT semantics if inserting duplicates.
6. If a person does not exist return 404


# What we are evaluating

Whenever you start a new position, you encounter code other people have written. You'll have to understand the architecture, write code to match it, and improve it for the next engineer. We are looking for:

- How do you approach writing a new feature? 
- Does your code do what it's supposed to do without obvious errors or bugs?
- Can you debug a problem in some unfamiliar code? How did you go about debugging?
- Can you evaluate, review, and improve upon code that is either poor or perhaps difficult to understand and maintain.

*💡 There are no right or wrong answers to the concepts above, but we're interested in your thinking, arguments & results.*

# What we are not evaluating

- Obtuse or complex python language features or skills.
    
We are a python shop and expect you to have a basic understanding of python language features (or can learn them quickly), particularly those found in many other modern languages. 

Hint: Brush up on classes, functions, loops, if-else control flow, iterators, dictionaries, lists, tuples, datetime.date

*This challenge should not require in-depth python knowledge or a deep understanding of any third-party Library. To that end, here are is a quick [Cheat sheet](#cheat-sheet) designed to get you over hurdles that are not particularly part of this evaluation*

# Cheat Sheet

```python

#### DEBUGGING WITH PRINT STATEMENTS ####
# print to console with flask app
app.logger.info("some string")

#### FLASK SQL ALCHEMY ####

# Get all persons
persons:list[Person] = Person.query.all()

# Pagination
persons:list[Person] = Person.query.limit(10).offset(10).all()

# Get person by id
person: Person = Person.query.get(id)

# Get Person by first name
persons:list[Person] = Person.query.filter_by(first_name='John').all()

# Sql Alchemy or_
from sqlalchemy import or_
persons: list[Person] = Person.query.filter(
    or_(Person.first_name == "Marcus", Person.first_name == "Keith")
).all()

# Run a raw query
from sqlalchemy.sql import text
from service.server import db

statement = text(
    """
    select id, first_name, middle_name, last_name from persons where first_name = 'Marcus';
    """
)
res: list = db.engine.execute(statement).all()
print(res[0]._asdict())

##### POSTGRES ####

# PSQL through docker (so that you do not have to download postgres to you machine)
docker run -it --rm --network coding_challenge postgres psql --host=db --port=5432 --username=noyo  --dbname=coding_challenge

# list tables
\dt
```

# Submission Options

You have two options for completing the exercise; choose the one that you are most comfortable with:

1. Zip up your code and email it to coding-challenge@noyo.com

2. Commit your code to a Github repository and share the link to the code in an email to coding-challenge@noyo.com

- **Note: Please do not fork this repository or open a pull request with your submission against this repository.**

## Support

If you have any issues or questions about the instructions below, please email **coding-challenge@noyo.com**, and we will get back to you as soon as possible.

## Live Extensions

We will ask you to implement one or more extensions to the code during your live coding interview. You are welcome to look at them, and encouraged to do so. However, you need not spend additional time implementing them beforehand.
- [Extension One: Get Address by Date](/docs/extension_one.md)
- [Extension Two: Merge Segments](/docs/extension_two.md)

## Instructions For Running

Here at Noyo we rely on [Docker Compose](https://docs.docker.com/compose/) to ensure the portability of our applications. We've provided a `docker-compose.yml` that installs all the appropriate dependencies and creates a database to which the application can connect.


### Building the App

You can build the server and database containers using the following command:

```bash

docker compose build

```

### Running the App

You can start the server and database using the following command:

```bash

docker compose up -d

```

This will start up the [Python Flask](https://flask.palletsprojects.com/en/1.1.x/) server on `localhost:3000` and a PostgreSQL instance on `localhost:5432`.

Flask starts up in debug mode, meaning whenever you save a file, it will restart the server with your changes.

### Running the Tests

We have provided a test suite that uses [pytest](https://docs.pytest.org/en/stable/). You can run the test suite using the following:

```bash

docker compose exec service pytest .

```

- *Note: The tests use the same database as the local server. When you run tests, the database is cleared of all data.**

### Seeding the Database

To make it easier to work with the API, we've provided a simple Python script that you can run to create five random `person` entries in the database. You can run the seed using the following:

```bash

docker-compose exec service python seed.py

```

- *Note: You can only run the seed after you have started the server using `docker-compose up`*

### Connecting to the database

The schema for the database is created for you when you start up the container by executing the contents of [`schema.sql`](/schema.sql). 

|Parameter|Value|
| ----------- | ----------- |
|Host|127.0.0.1|
|Port|5432
|Database|coding_challenge|
|Username|noyo|
|Password|noyo|

```shell
docker run -it --rm --network coding_challenge postgres psql --host=db --port=5432 --username=noyo  --dbname=coding_challenge
```
### Formatting your Code

We use [Black](https://github.com/psf/black) to handle the formatting of our code. Black enables you to spend less time worrying about spacing and indents during code reviews and more time focusing on the content. If you would like to format your code using Black, you can run the following command:

```bash

docker compose exec service black .

```


### Debugging
If you would like to step into and debug code, and are familiar with visual studio code, we have included a [devcontainer.json](/.devcontainer/devcontainer.json). On the the bottom left of vs code there is a button with two angle brackets "><"  

![Open Remote Container](/docs/remote.png)  

Click that button and it will bring up a menu that you can "Reopen in container". Clicking that will run vs code attached to the docker container with a the virtual python environment setup for you. From there you will be able to setup a nice unit test environment.

![Screenshot](/docs/tests.png)  

### Starting Over

If you get your database or local server into a weird state, you can start anew by running:

```bash

docker-compose down --remove-orphans --volumes

```

Then go back to [Running the App](#running-the-app) and start over.

# Thanks!

We make every effort to demonstrate that we see your time as valuable. We will make every attempt throughout the interview process not to waste it. Nonetheless, we know you're making a big-time commitment. We're sincerely appreciative of both your time and your interest in working with the team at Noyo.
