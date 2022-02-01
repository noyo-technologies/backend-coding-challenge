import pytest
import uuid

from datetime import timedelta

from service.models import Segment, Person

from service.server import db
from flask.testing import FlaskClient
from flask.ctx import AppContext


@pytest.fixture
def seed_person():
    person = Person(
        first_name="John",
        last_name="Doe"        
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    yield person


@pytest.fixture
def seed_segment_segment(seed_person):
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


def test_create_segment_with_validation_error(test_context: AppContext, client: FlaskClient, seed_person: Person):
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


def test_create_single_valid_segment(test_context: AppContext, client: FlaskClient, seed_person: Person):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/segment",
            json={
                "start_date": "2021-01-01",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )

        assert response.status_code == 200


def test_get_segment(test_context: AppContext, client: FlaskClient, seed_segment_segment: Segment):
    with test_context:
        response = client.get(f"/api/persons/{seed_segment_segment.person_id}/segment")
        assert response.status_code == 200


def test_get_segment_no_person(test_context: AppContext, client: FlaskClient):
    with test_context:
        response = client.get(f"/api/persons/{uuid.uuid4()}/segment")
        assert response.status_code == 404
        assert response.json == {"error": "person does not exist"}


def test_get_segment_no_segment_exists(test_context: AppContext, client: FlaskClient, seed_person: Person):
    with test_context:
        response = client.get(f"/api/persons/{seed_person.id}/segment")
        assert response.status_code == 404
        assert response.json == {
            "error": "person does not have an segment, please create one"
        }


def test_create_initial_segment_segment(test_context: AppContext, client: FlaskClient, seed_person: Person):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/segment",
            json={
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
                "start_date": "2021-06-15",
            },
        )

        assert response.status_code == 200
        assert response.json == {
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94613",
            "start_date": "2021-06-15",
            "end_date": None,
        }


def test_implementation_create_and_update_segment(
    test_context: AppContext, client: FlaskClient, seed_segment_segment: Segment
):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_segment_segment.person_id}/segment",
            json={
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94111",
                "start_date": "2021-06-15",
            },
        )
        assert response.status_code == 200
        assert response.json == {
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94111",
            "start_date": "2021-06-15",
            "end_date": None,
        }
