from uuid import uuid4
from faker import Faker
from service.server import db

from service.models import Person

fake = Faker()
persons = []
for _ in range(5):
    persons.append(
        Person(
            id=uuid4(),
            first_name=fake.first_name(),
            middle_name=fake.first_name(),
            last_name=fake.last_name(),
        )
    )

db.session.add_all(persons)
db.session.commit()
