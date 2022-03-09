from uuid import UUID
from flask import abort, jsonify
from webargs.flaskparser import use_args
from marshmallow import Schema, fields

from service.server import app, db
from service.models import Person


###### Validation Schemas ######
class UpdateOrFindPersonSchema(Schema):
    first_name = fields.Str(max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(max=128)


class CreatePersonSchema(Schema):
    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)


###### Response Schemas ######
class PersonResonseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)
    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)


@app.route("/api/persons", methods=["GET"])
@use_args(UpdateOrFindPersonSchema(), location="query")
def get_persons(args: dict):
    persons = Person.query.filter_by(**args).order_by(Person.last_name.asc()).all()
    return jsonify(PersonResonseSchema(many=True).dump(persons))


@app.route("/api/persons/<uuid:id>", methods=["GET"])
def get_person(id: UUID):
    # Check if a person exists and abort 404 if not found
    person = Person.query.get(id)
    if person is None:
        abort(404, description="person does not exist")

    return jsonify(PersonResonseSchema().dump(person))


@app.route("/api/persons", methods=["POST"])
@use_args(CreatePersonSchema())
def create_person(payload: dict):
    person = Person(
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        middle_name=payload.get("middle_name"),
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    return jsonify(PersonResonseSchema().dump(person))


@app.route("/api/persons/<uuid:id>", methods=["PATCH"])
@use_args(UpdateOrFindPersonSchema())
def update_person(payload: dict, id: UUID):
    # Check if a person exists and abort 404 if not found
    person = db.session.query(Person).get(id)
    if person is None:
        abort(404, description="person does not exist")

    # loop over items and set attributes
    for update_key, update_value in payload.items():
        setattr(person, update_key, update_value)

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    return jsonify(PersonResonseSchema().dump(person))
