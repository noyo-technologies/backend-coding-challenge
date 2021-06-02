from flask import abort, jsonify
from webargs.flaskparser import use_args

from marshmallow import Schema, fields

from service.server import app, db
from service.models import Person


class CreatePersonSchema(Schema):
    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)
    email = fields.Email(required=True, max=128)
    date_of_birth = fields.Date(required=True)


class PersonResultSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)
    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)
    email = fields.Email(required=True, max=128)
    date_of_birth = fields.Date(required=True)


class UpdatePersonSchema(Schema):
    first_name = fields.Str(max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(max=128)
    email = fields.Email(max=128)
    date_of_birth = fields.Date()


@app.route("/api/persons", methods=["GET"])
def get_persons():
    persons = Person.query.order_by(Person.id.asc()).all()
    return jsonify(PersonResultSchema(many=True).dump(persons))


@app.route("/api/persons/<uuid:id>", methods=["GET"])
def get_person(id):
    person = Person.query.get(id)
    if person is None:
        abort(404, description="person does not exist")

    return jsonify(PersonResultSchema().dump(person))


@app.route("/api/persons", methods=["POST"])
@use_args(CreatePersonSchema())
def create_person(payload):
    person = Person(
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        middle_name=payload.get("middle_name"),
        email=payload.get("email"),
        date_of_birth=payload.get("date_of_birth"),
    )

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    return jsonify(PersonResultSchema().dump(person))


@app.route("/api/persons/<uuid:id>", methods=["PATCH"])
@use_args(UpdatePersonSchema())
def update_person(payload, id):
    person = db.session.query(Person).get(id)
    if person is None:
        abort(404, description="person does not exist")

    for update_key, update_value in payload.items():
        setattr(person, update_key, update_value)

    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)

    return jsonify(PersonResultSchema().dump(person))
