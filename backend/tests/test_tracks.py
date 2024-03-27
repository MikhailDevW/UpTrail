import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

valid_data = [
    ({"lt_lat": -55}, status.HTTP_200_OK),
]


@pytest.fixture
def client_login():
    # Логинимся для получения токена
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    # assert response.status_code == status.HTTP_200_OK, (
    #     "Проверьте, что запрос на логин возвращает ответ со статусом 200"
    # )
    # token = response.json()["access_token"]
    token = "vdssdfsdfsd"
    # Добавляем токен в заголовки для авторизации
    headers = {"Authorization": f"Bearer {token}"}

    return headers


class TestTrack:

    @pytest.mark.parametrize(["params", "result",], valid_data)
    def test_track_not_auth(self, params, result):
        "Тестируем модуль треков неавторизованным пользователем."
        response = client.get("/tracks/get_tracks", params=params,)
        assert response.status_code != status.HTTP_404_NOT_FOUND, (
            'Эндпоинт не найден, проверьте роуты.'
        )
        assert response.status_code == status.HTTP_200_OK, (
            "Проверьте, что запрос возвращает ответ со статусом 200"
        )
        assert response.json() == {
            "latitue": 54.3,
            "longitute": 54.3,
            "distance": 13,
        }

        response = client.post("tracks/post_track")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            "Проверьте, что доступ к публикации трека есть только "
            "у авторизованного пользователя."
        )

        response = client.patch("track/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            "Проверьте, что доступ на редактирование есть только "
            "у авторизованного пользователя."
        )

        response = client.delete("track/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            "Проверььте, что доступ на удаление етсь только "
            "у авторизованного пользователя."
        )

    def test_track_auth(self, client_login):
        # можем отправить запрос, требующий авторизации
        response = client.get("tracks/post_track", headers=client_login)
        assert response.status_code == status.HTTP_200_OK
