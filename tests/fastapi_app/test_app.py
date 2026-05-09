from fastapi.testclient import TestClient


class TestApp:
    def test_status__app_running__valid_response(self, test_client: TestClient):
        """
        Проверка статуса приложения в нормальном сценарии с ожидаем ответа по умолчанию
        """

        # Действие
        response = test_client.get('/api/status')

        # Проверка
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
