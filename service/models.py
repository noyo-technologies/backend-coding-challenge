import uuid

from sqlalchemy.dialects.postgresql import UUID

from service.server import db


class Person(db.Model):
    __tablename__ = "persons"

    address_segments = db.relationship(
        "AddressSegment", order_by="desc(AddressSegment.start_date)"
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    first_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)


class AddressSegment(db.Model):
    __tablename__ = "address_segments"

    person_id = db.Column(UUID(as_uuid=True), db.ForeignKey("persons.id"))

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    street_one = db.Column(db.String(128), nullable=False)
    street_two = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=True)
