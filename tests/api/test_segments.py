import pytest
import uuid

from datetime import date, timedelta

from service.models import Segment, Person

from service.server import db
from flask.testing import FlaskClient
from flask.ctx import AppContext


@pytest.fixture
def seed_person( test_context: AppContext):
    with  test_context:
        """seed and return a person"""
        person = Person(first_name="John", last_name="Doe")

        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)

        yield person


@pytest.fixture
def seed_person_and_segment(seed_person: Person):
    """seed a person (via the seed_person fixture) and a seed a single segment"""
    segment_segment = Segment(
        city="San Francisco",
        state="CA",
        zip_code="94613",
        start_date="2021-01-01",
        person_id=seed_person.id,
    )
    db.session.add(segment_segment)
    db.session.commit()
    db.session.refresh(segment_segment)

    yield segment_segment


def test_create_segment_with_validation_error(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        response = client.put(f"/api/persons/{seed_person.id}/segment", json={})

        assert response.status_code == 422
        assert response.json == {
            "errors": {
                "json": {
                    "city": ["Missing data for required field."],
                    "start_date": ["Missing data for required field."],
                    "state": ["Missing data for required field."],
                    "zip_code": ["Missing data for required field."],
                }
            }
        }


def test_get_segment(
    test_context: AppContext, client: FlaskClient, seed_person_and_segment: Segment
):
    with test_context:
        response = client.get(
            f"/api/persons/{seed_person_and_segment.person_id}/segment"
        )
        assert response.status_code == 200


def test_get_segment_no_person(test_context: AppContext, client: FlaskClient):
    with test_context:
        response = client.get(f"/api/persons/{uuid.uuid4()}/segment")
        assert response.status_code == 404
        assert response.json == {"error": "person does not exist"}


def test_get_segment_no_segment_exists(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        response = client.get(f"/api/persons/{seed_person.id}/segment")
        assert response.status_code == 404
        assert response.json == {
            "error": "person does not have an segment, please create one"
        }
