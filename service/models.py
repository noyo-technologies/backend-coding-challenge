import uuid

from sqlalchemy.dialects.postgresql import UUID

from service.server import db


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    first_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=False)

    # sql alchemy will populate this attribute as a list
    # of all segments that have Segment.person_id == Person.id
    segments = db.relationship("Segment")


class Segment(db.Model):
    __tablename__ = "segments"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())

    person_id = db.Column(UUID(as_uuid=True), db.ForeignKey("persons.id"))

    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=True)

    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
