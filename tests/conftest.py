import pytest


from service.server import app
from service.server import db
from service.models import Segment, Person


@pytest.fixture
def client():
    client = app.test_client()

    yield client


@pytest.fixture
def test_context():
    app_context = app.app_context()

    yield app_context


def pytest_runtest_teardown():
    with app.app_context():
        model_class_list = [Segment, Person]

        for model in model_class_list:
            db.session.query(model).delete()
            db.session.commit()
