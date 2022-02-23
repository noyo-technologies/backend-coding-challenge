# Debugging with print statments
```python
# print to console with flask app
app.logger.info("some string")
```

# Curl Commands
```sh
# PUT
curl -X PUT \
  http://localhost:3000/api/persons/8abbc8e0-7039-4988-8a20-e6c1e1b3bb2f/segment \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2021-04-15",
    "end_date": "2021-08-15",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94911"
  }'

# GET
curl http://localhost:3000/api/persons
```


# Flask SQL Alchemy
We use sqlalchemy at noyo but do not expect that to have worked with it, as such here is the simple crash course on it. Please note that no sqlalchemy code is required to solve any of the problems or extenstions. This is here solely for your reference.


### Add a person
```python
# insert into person (first_name, last_name) values ('John', 'Doe');
person = Person(
    first_name="John",
    last_name="Doe"
)

db.session.add(person)
db.session.commit()
```

### Delete Person
```python
# delete from persons WHERE id = %1;
db.session.delete(person)
db.session.commit()
```

### Get all persons
```python
# select * from persons;
persons = Person.query.all()
```

### Get person by id
```python
# select * from persons where id = %1;
person = Person.query.get(id)
```

### Get Person by first name
```python
# select * from persons where first_name='John';
persons = Person.query.filter_by(first_name='John').all()
```

# Postgres 

### PSQL through docker 
```sh
# so that you do not have to download postgres to you machine
docker run -it --rm --network coding_challenge postgres psql --host=db --port=5432 --username=noyo  --dbname=coding_challenge
```