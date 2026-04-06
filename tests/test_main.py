import pytest
from unittest.mock import AsyncMock


def test_get_rates_success(mocker, client):
    mock_rates = {"usd": 90.5, "eur": 98.2,
                  "gbp": 115.3, "jpy": 0.62, "chf": 102.4}
    mocker.patch("app.main.fetch_rates", AsyncMock(return_value=mock_rates))
    response = client.get("/rates")
    assert response.status_code == 200
    data = response.json()
    assert data["usd"] == 90.5


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
    client.get("/rates")
    response = client.get("/stats")
    assert response.json()["total_requests"] == 1
