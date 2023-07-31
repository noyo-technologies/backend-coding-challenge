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

# Marshmallow
Marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.

```python
class ArtistSchema(Schema):
    name = fields.Str(required=True)

@app.route("/api/some_route", methods=["POST"])
@use_args(ArtistSchema())
def some_route(payload: dict):
    # marshmallow will validate the incomming POST payload, 
    # ensuring that there is a valid string value.
    return payload["name"]
```

# Flask SQLAlchemy
We use [SQLAlchemy](https://www.sqlalchemy.org/) at Noyo, but do not expect you to have worked with it, as such here is the simple crash course on it. Please note that no advanced SQLAlchemy code is required to solve any of the problems or extensions. For example, in lieu of using the `.filter_by` syntax feel free to load models into memory and to filter using pure Python. 


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
So that you do not have to download postgres to your machine, you can run the following command to get a psql command prompt into the database
```sh
docker run -it --rm --network coding_challenge postgres psql --host=db --port=5432 --username=noyo  --dbname=coding_challenge
```