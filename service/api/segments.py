from datetime import datetime
from uuid import UUID

from flask import abort, jsonify
from webargs.flaskparser import use_args

from marshmallow import Schema, fields

from service.server import app
from service.models import Person

###### Query Schemas ######
class GetSegmentQueryArgsSchema(Schema):
    date = fields.Date(required=False, missing=datetime.utcnow().date())


###### Validation and Response Schemas ######
class SegmentSchema(Schema):
    class Meta:
        ordered = True

    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)


@app.route("/api/persons/<uuid:person_id>/segment", methods=["GET"])
@use_args(GetSegmentQueryArgsSchema(), location="querystring")
def get_segment(args: dict, person_id: UUID):
    person = Person.query.get(person_id)

    if person is None:
        abort(404, description="person does not exist")
    elif len(person.segments) == 0:
        abort(404, description="person does not have an segment, please create one")

    # query date comes in the the args and default to "today"
    query_date = args["date"]

    # Just get the the first segment that comes back
    segment = person.segments[0]
    return jsonify(SegmentSchema().dump(segment))


@app.route("/api/persons/<uuid:person_id>/merge", methods=["PUT"])
@use_args(SegmentSchema())
def merge_segments(payload: dict, person_id: UUID):
    return "Not Implemented", 501


@app.route("/api/persons/<uuid:person_id>/segment", methods=["PUT"])
@use_args(SegmentSchema())
def create_segment(payload: dict, person_id: UUID):
    return "Not Implemented", 501
