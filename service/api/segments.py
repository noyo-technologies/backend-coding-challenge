from datetime import datetime
from uuid import UUID

from flask import abort, jsonify, request
from webargs.flaskparser import use_args

from marshmallow import Schema, fields

from service.server import app, db
from service.models import Person, Segment


# Query Schemas
class GetSegmentQueryArgsSchema(Schema):
    date = fields.Date(required=False, missing=datetime.utcnow().date())
    limit = fields.Bool(required=False, missing=False)


# Validation and Response Schemas
class SegmentSchema(Schema):
    class Meta:
        ordered = True

    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)


# Response Schemas
class SegmentResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)
    person_id = fields.UUID(required=True)
    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)


@app.route("/api/persons/<uuid:person_id>/segments", methods=["GET"])
@use_args(GetSegmentQueryArgsSchema(), location="querystring")
def get_segments(args: dict, person_id: UUID):
    """Get segment(s) for person.

    Args:
    ----
        args (dict): optional arguments for refinement of the query
            date: use a date other than today
            limit: (BOOL) whether to show all segments for that date, or just one
        person_id (UUID): unique id of the person, stored in the database.

    Returns:
    -------
        _type_: _description_

    Notes:
    -----
    This API should use the plural of segment instead.
    This would be more consistent with the REST rules and existing URI's.

    I'm going to make the change based on the assumption that this API
    is not yet being used. However, if this API is already being used
    by clients, we dont want to change it on them. Instead, we could
    create a strategy to change it in future versions and include
    deprecation messages in the existing API, and ensure that the
    breaking change is communicated in the notes of future versions of the API
    """
    person = get_person_by_id(person_id)
    if person is None:
        abort(404, description="person does not exist")
    elif len(person.segments) == 0:
        abort(404, description="person does not have a segment, please create one")

    # query date comes in the the args and default to "today"
    query_date = args["date"]

    limit = args["limit"]

    if limit:
        # if the limit is true, only send the last item in a sequence
        # for future, using "range" could allow for number
        # of items to retrieve/show
        segments = [person.segments[-1]]
    else:
        # otherwise default to all segments
        segments = person.segments
    return jsonify(SegmentResponseSchema(many=True).dump(segments))


@app.route("/api/persons/<uuid:person_id>/segments", methods=["PUT"])
@use_args(SegmentSchema())
def upsert_segment(payload: dict, person_id: UUID):
    """Insert or update segment based on:
        * if no segments for the person. CREATE NEW
        * if new segment start date is:
            * same as latest segment start date: UPDATE EXISTING
            * earlier than latest segment end date: FAIL
            * later than latest segment start date, and end date is null:
                UPDATE EXISTING, & CREATE NEW
            * later than latest segment end date: CREATE NEW

    Args:
        payload (dict): _description_
        person_id (UUID): _description_

    Returns:
        _type_: _description_
    """
    person = get_person_by_id(person_id)
    if person is None:
        abort(404, description="No person found for segment")

    new_segment_data = fill_segment(payload, person_id)

    if len(person.segments) == 0:
        # if there are no segments for this person,
        # then create the first one
        new_segment = create_segment(new_segment_data)
        return jsonify(SegmentResponseSchema().dump(new_segment))

    # otherwise get the latest segment
    previous_segment = person.segments[-1]

    if new_segment_data.start_date == previous_segment.start_date:
        updated_segment = update_segment(new_segment_data, previous_segment.id)
        return jsonify(SegmentResponseSchema().dump(updated_segment))

    if new_segment_data.start_date < previous_segment.start_date:
        # if new segment's start date is before the previous_segment's start date
        abort(422, description="new segment starts before previous segment ends")

    if not previous_segment.end_date:
        # update the latest segment with an end date
        # which will be the same as the new segment start date
        previous_segment.end_date = new_segment_data.start_date
        updated_segment = update_segment(previous_segment, previous_segment.id)

        # and create new segment
        new_segment = create_segment(new_segment_data)
        return jsonify(SegmentResponseSchema().dump(new_segment))
    elif new_segment_data.start_date < previous_segment.end_date:
        # if new segment's start date is before the previous_segment's end date
        abort(422, description="new segment starts before previous segment ends")
    else:
        new_segment = create_segment(new_segment_data)
        return jsonify(SegmentResponseSchema().dump(new_segment))


    # this should never trigger
    app.logger.warn(f"Failed to upsert segment for person: {person_id}")


def update_segment(segment, id):
    """Connect to DB and update existing segment for person"""
    segment_to_update = db.session.query(Segment).get(id)

    db.session.add(segment_to_update)
    db.session.commit()
    db.session.refresh(segment_to_update)
    return segment_to_update


def create_segment(segment: Segment):
    """Connect to DB and create new segment for person"""
    db.session.add(segment)
    db.session.commit()
    db.session.refresh(segment)
    return segment


def fill_segment(payload: dict, person_id: UUID):
    """Create new segment based on Segment model"""
    return Segment(
        person_id=person_id,
        city=payload.get("city"),
        state=payload.get("state"),
        zip_code=payload.get("zip_code"),
        start_date=payload.get("start_date"),
        end_date=payload.get("end_date"),
    )


def get_person_by_id(person_id):
    return Person.query.get(person_id)
