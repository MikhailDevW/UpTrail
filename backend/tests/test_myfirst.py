from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_track():
    response = client.get("/tracks/get_tracks")
    assert response.status_code == 200


def test_hello():
    assert 1 == 1, "Number is not equal"
