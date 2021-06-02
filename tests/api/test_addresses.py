import pytest
import uuid

from datetime import timedelta

from service.models import AddressSegment, Person

from service.server import db


@pytest.fixture
def seed_person():
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth="1978-06-12",
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    yield person


@pytest.fixture
def seed_address_segment(seed_person):
    address_segment = AddressSegment(
        street_one="123 Main Street",
        city="San Francisco",
        state="CA",
        zip_code="94613",
        start_date="2021-01-01",
        person_id=seed_person.id,
    )
    db.session.add(address_segment)
    db.session.commit()
    db.session.refresh(address_segment)

    yield address_segment


def test_create_address_with_validation_error(test_context, client, seed_person):
    with test_context:
        response = client.put(f"/api/persons/{seed_person.id}/address", json={})

        assert response.status_code == 422
        assert response.json == {
            "errors": {
                "json": {
                    "city": ["Missing data for required field."],
                    "start_date": ["Missing data for required field."],
                    "state": ["Missing data for required field."],
                    "street_one": ["Missing data for required field."],
                    "zip_code": ["Missing data for required field."],
                }
            }
        }


def test_create_single_valid_address(test_context, client, seed_person):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/address",
            json={
                "start_date": "2021-01-01",
                "street_one": "123 Main Street",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
            },
        )

        assert response.status_code == 200


def test_get_address(test_context, client, seed_address_segment):
    with test_context:
        response = client.get(f"/api/persons/{seed_address_segment.person_id}/address")
        assert response.status_code == 200


def test_get_address_no_person(test_context, client):
    with test_context:
        response = client.get(f"/api/persons/{uuid.uuid4()}/address")
        assert response.status_code == 404
        assert response.json == {"error": "person does not exist"}


def test_get_address_no_address_exists(test_context, client, seed_person):
    with test_context:
        response = client.get(f"/api/persons/{seed_person.id}/address")
        assert response.status_code == 404
        assert response.json == {
            "error": "person does not have an address, please create one"
        }


def test_create_initial_address_segment(test_context, client, seed_person):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_person.id}/address",
            json={
                "street_one": "123 Main Street",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94613",
                "start_date": "2021-06-15",
            },
        )

        assert response.status_code == 200
        assert response.json == {
            "street_one": "123 Main Street",
            "street_two": None,
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94613",
            "start_date": "2021-06-15",
            "end_date": None,
        }


def test_implementation_create_and_update_address(
    test_context, client, seed_address_segment
):
    with test_context:
        response = client.put(
            f"/api/persons/{seed_address_segment.person_id}/address",
            json={
                "street_one": "1 California Street",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94111",
                "start_date": "2021-06-15",
            },
        )
        assert response.status_code == 200
        assert response.json == {
            "street_one": "1 California Street",
            "street_two": None,
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94111",
            "start_date": "2021-06-15",
            "end_date": None,
        }


# TODO: Extension One
# def test_extension_one_validation_of_same_start_date(test_context, client, seed_address_segment):
#     with test_context:
#         # Update the existing address using the person_id and start_date from the
#         # already existing, seed_address_segment
#         response = client.put(
#             f"/api/persons/{seed_address_segment.person_id}/address", json={
#                 "street_one": "123 Main Street",
#                 "city": "San Francisco",
#                 "state": "CA",
#                 "zip_code": "94613",
#                 "start_date": seed_address_segment.start_date.isoformat()
#             }
#         )
#         assert response.status_code == 422
#         assert response.json == {
#             "error": "Address segment already exists with start_date 2021-01-01"
#         }

# TODO: Extension Two
# def test_extension_two_get_address_by_date(test_context, client, seed_address_segment):
#     with test_context:
#         start_date = seed_address_segment.start_date
#         new_start_date = start_date + timedelta(days=90)
#         response = client.put(
#             f"/api/persons/{seed_address_segment.person_id}/address", json={
#                 "street_one": "1 California Street",
#                 "city": "San Francisco",
#                 "state": "CA",
#                 "zip_code": "94111",
#                 "start_date": new_start_date.isoformat()
#             }
#         )
#         assert response.status_code == 200

#         first_get_response = client.get(f"/api/persons/{seed_address_segment.person_id}/address", query_string={"date": start_date.isoformat()})
#         assert first_get_response.status_code == 200
#         assert first_get_response.json["street_one"] == seed_address_segment.street_one

#         second_get_response = client.get(f"/api/persons/{seed_address_segment.person_id}/address?date={new_start_date.isoformat()}")
#         assert second_get_response.status_code == 200
#         assert second_get_response.json["street_one"] == "1 California Street"

# TODO: Extension Three
# def test_extension_three_merge_contiguous_equal_addresses(test_context, client, seed_address_segment):
#     with test_context:
#         start_date = seed_address_segment.start_date
#         new_start_date = start_date + timedelta(days=90)
#         response = client.put(
#             f"/api/persons/{seed_address_segment.person_id}/address", json={
#                 "street_one": seed_address_segment.street_one,
#                 "city": seed_address_segment.city,
#                 "state": seed_address_segment.state,
#                 "zip_code": seed_address_segment.zip_code,
#                 "start_date": new_start_date.isoformat()
#             }
#         )
#         assert response.status_code == 200

#         person = Person.query.get(seed_address_segment.person_id)
#         assert len(person.address_segments) == 1
