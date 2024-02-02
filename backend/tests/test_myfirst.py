# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_get_track():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {
#         'name': 'track_name',
#         'author': 'DocLivesey',
#         'comment': 'my comment',
#         'start_langtitude': 56.3,   # coordiante
#         'start_latitude': 56.3,     # coordinate
#         'distance': 50,             # in km?
#         'duration': 1,              # datetime format?
# }


def test_hello():
    assert 1 == 1, 'Number is not equal'
