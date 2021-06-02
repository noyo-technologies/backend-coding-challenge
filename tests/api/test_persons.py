import uuid

from service.models import Person

from service.server import db


def test_create_person_with_validation_error(test_context, client):
    with test_context:
        create_response = client.post("/api/persons", json={})

        assert create_response.status_code == 422
        assert create_response.json == {
            "errors": {
                "json": {
                    "date_of_birth": ["Missing data for required field."],
                    "email": ["Missing data for required field."],
                    "first_name": ["Missing data for required field."],
                    "last_name": ["Missing data for required field."],
                }
            }
        }


def test_create_person_success(test_context, client):
    with test_context:
        create_response = client.post(
            "/api/persons",
            json={
                "first_name": "John",
                "middle_name": "J",
                "last_name": "Doe",
                "email": "john@example.com",
                "date_of_birth": "1980-01-15",
            },
        )

        assert create_response.status_code == 200
        assert create_response.json["first_name"] == "John"
        assert create_response.json["middle_name"] == "J"
        assert create_response.json["last_name"] == "Doe"
        assert create_response.json["email"] == "john@example.com"
        assert create_response.json["date_of_birth"] == "1980-01-15"


def test_get_person_not_found(test_context, client):
    with test_context:
        get_response = client.get(f"/api/persons/{uuid.uuid4()}")

        assert get_response.status_code == 404
        assert get_response.json == {"error": "person does not exist"}


def test_get_person_success(test_context, client):
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1978-06-12",
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    with test_context:
        get_response = client.get(f"/api/persons/{person.id}")

        assert get_response.status_code == 200
        assert get_response.json == {
            "id": str(person.id),
            "first_name": "John",
            "middle_name": None,
            "last_name": "Doe",
            "email": "john@example.com",
            "date_of_birth": "1978-06-12",
        }


def test_get_persons_success(test_context, client):
    person_one = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1990-06-22",
    )
    person_two = Person(
        first_name="Jane",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1990-06-22",
    )

    db.session.add(person_one)
    db.session.add(person_two)
    db.session.commit()

    with test_context:
        get_response = client.get("/api/persons")

        assert get_response.status_code == 200
        assert len(get_response.json) == 2


def test_patch_person_with_validation_error(test_context, client):
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1990-06-22",
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    with test_context:
        patch_response = client.patch(
            f"/api/persons/{person.id}", json={"first_name": None, "last_name": None}
        )

        assert patch_response.status_code == 422
        assert patch_response.json == {
            "errors": {
                "json": {
                    "first_name": ["Field may not be null."],
                    "last_name": ["Field may not be null."],
                }
            }
        }


def test_patch_person_person_does_not_exist(test_context, client):
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1990-06-22",
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    with test_context:
        patch_response = client.patch(
            f"/api/persons/{uuid.uuid4()}", json={"first_name": "Jane"}
        )

        assert patch_response.status_code == 404
        assert patch_response.json == {"error": "person does not exist"}


def test_patch_person_success(test_context, client):
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1990-05-14",
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    with test_context:
        patch_response = client.patch(
            f"/api/persons/{person.id}",
            json={"last_name": "Smith", "email": "john.smith@example.com"},
        )

        assert patch_response.status_code == 200
        assert patch_response.json == {
            "id": str(person.id),
            "first_name": "John",
            "middle_name": None,
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "date_of_birth": "1990-05-14",
        }
