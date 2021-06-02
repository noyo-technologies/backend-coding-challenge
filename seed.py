import requests

from faker import Faker

fake = Faker()

for _ in range(5):
    first_name = fake.first_name()
    last_name = fake.last_name()
    payload = {
        "first_name": first_name,
        "middle_name": fake.first_name(),
        "last_name": last_name,
        "email": f"{first_name}.{last_name}@example.com".lower(),
        "date_of_birth": fake.date(),
    }

    response = requests.post("http://localhost:3000/api/persons", json=payload)
    response.raise_for_status()

    person = response.json()

    print("-" * 100)
    print(f"Created Person: {person['first_name']} {person['last_name']}")
    print(person["id"])
