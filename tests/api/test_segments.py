import pytest
import uuid

from datetime import date, timedelta

from service.models import Segment, Person

from service.server import db
from flask.testing import FlaskClient
from flask.ctx import AppContext


@pytest.fixture
def seed_person(test_context: AppContext):
    with test_context:
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


@pytest.fixture
def segment_data():
    return {
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94613",
        "start_date": "2021-01-01",
    }


def test_create_segment_with_validation_error(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/segments?limit=true", json={}
        )

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
            f"/api/persons/{seed_person_and_segment.person_id}/segments?limit=true"
        )
        assert response.status_code == 200


def test_get_segment_no_person(test_context: AppContext, client: FlaskClient):
    with test_context:
        response = client.get(f"/api/persons/{uuid.uuid4()}/segments?limit=true")
        assert response.status_code == 404
        assert response.json == {"error": "person does not exist"}


def test_get_segment_no_segment_exists(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        response = client.get(f"/api/persons/{seed_person.id}/segments?limit=true")
        assert response.status_code == 404
        assert response.json == {
            "error": "person does not have a segment, please create one"
        }


def test_add_segment(
    test_context: AppContext,
    client: FlaskClient,
    seed_person: Person,
    segment_data: dict,
):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/segments?limit=true",
            json=segment_data,
        )
    assert response.status_code == 200
    assert response.json["start_date"] == "2021-01-01"
    assert response.json["city"] == "San Francisco"
    assert response.json["state"] == "CA"
    assert response.json["person_id"] == str(seed_person.id)


def test_add_segment_user_not_found(
    test_context: AppContext, client: FlaskClient, segment_data: dict
):
    with test_context:
        response = client.put(
            f"/api/persons/{uuid.uuid4()}/segments?limit=true",
            json=segment_data,
        )
        assert response.status_code == 404
        assert response.json == {"error": "No person found for segment"}


def test_add_two_segments(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    # this simply tests that we can add two segments for each user,
    # as long as their start dates and end dates arte correct
    with test_context:
        uri = f"/api/persons/{seed_person.id}/segments"
        response1 = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "end_date": "2021-01-02",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )
        response2 = client.put(
            uri,
            json={
                "start_date": "2021-01-03",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "94444",
            },
        )
        all_segments = client.get(f"{uri}?limit=false")

    assert response1.status_code == 200
    assert response1.json["city"] == "San Francisco"
    assert response1.json["start_date"] == "2021-01-01"

    assert response2.status_code == 200
    assert response2.json["city"] == "Los Angeles"
    assert response2.json["start_date"] == "2021-01-03"

    assert len(all_segments.json) > 1


def test_update_segment_existing(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        uri = f"/api/persons/{seed_person.id}/segments"
        segment_data = {
            "start_date": "2021-01-01",
            "end_date": "2021-01-02",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94613",
        }
        segment_call_1 = client.put(
            uri,
            json=segment_data,
        )
        segment_call_2 = client.put(
            uri,
            json=segment_data,
        )
    for key, value in segment_call_1.json.items():
        if not key == "id":
            assert value == segment_call_2.json[key]


def test_update_segment_no_end_date(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        uri = f"/api/persons/{seed_person.id}/segments"
        segment = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )
    assert segment.json["end_date"] is None


def test_add_two_segments_updating_end_date(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    with test_context:
        uri = f"/api/persons/{seed_person.id}/segments"
        segment_1 = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )
        segment_2 = client.put(
            uri,
            json={
                "start_date": "2021-01-02",
                "end_date": "2021-01-03",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "94518",
            },
        )
        all_segments = client.get(f"{uri}?limit=false")
    for segment in all_segments.json:
        if segment["zip_code"] == "94613":
            assert segment["end_date"] == "2021-01-02"


def test_update_segment_datetime_same_dates(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    uri = f"/api/persons/{seed_person.id}/segments"
    with test_context:
        original_segment = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "end_date": "2021-01-02",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )
        response = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "94518",
            },
        )
    assert response.status_code == 200
    assert response.json["id"] == original_segment.json["id"]


def test_update_segment_datetime_mistmatch(
    test_context: AppContext, client: FlaskClient, seed_person: Person
):
    uri = f"/api/persons/{seed_person.id}/segments"
    with test_context:
        original_segment = client.put(
            uri,
            json={
                "start_date": "2021-01-01",
                "end_date": "2021-01-03",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )
        response = client.put(
            uri,
            json={
                "start_date": "2021-01-02",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "94518",
            },
        )
    assert response.status_code == 422
