import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app

# client уже предоставлен фикстурой из conftest.py
# если conftest.py определён, то не нужно создавать client заново


def test_get_rates_success(mocker, client):
    mock_rates = {"usd": 90.5, "eur": 98.2,
                  "gbp": 115.3, "jpy": 0.62, "chf": 102.4}
    mocker.patch("app.main.fetch_rates", AsyncMock(return_value=mock_rates))

    response = client.get("/rates")
    assert response.status_code == 200
    data = response.json()
    assert data["usd"] == 90.5
    assert data["eur"] == 98.2


def test_get_rates_fail(mocker, client):
    mocker.patch("app.main.fetch_rates", AsyncMock(
        side_effect=Exception("API error")))
    response = client.get("/rates")
    assert response.status_code == 503


def test_get_stats_empty(client):
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total_requests"] == 0


def test_stats_after_request(mocker, client):
    mock_rates = {"usd": 90.5, "eur": 98.2,
                  "gbp": 115.3, "jpy": 0.62, "chf": 102.4}
    mocker.patch("app.main.fetch_rates", AsyncMock(return_value=mock_rates))

    resp1 = client.get("/rates")
    assert resp1.status_code == 200

    resp2 = client.get("/stats")
    assert resp2.status_code == 200
    # теперь точно 1, т.к. БД чистая
    assert resp2.json()["total_requests"] == 1
