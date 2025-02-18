import pytest
from fastapi.testclient import TestClient
from server import app

test_client = TestClient(app)

def test_get_expenses_valid_date():
    response = test_client.get("/expenses/2024-08-15")
    assert response.status_code in [200, 404]  
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)

def test_get_expenses_invalid_date():
    response = test_client.get("/expenses/invalid-date")
    assert response.status_code == 422  

def test_post_expenses():
    test_data = [
        {"amount": 15.0, "category": "Entertainment", "notes": "Movie"},
        {"amount": 30.0, "category": "Food", "notes": "Dinner"}
    ]
    response = test_client.post("/expenses/2024-08-16", json=test_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Expenses updated successfully"

def test_post_expenses_invalid_data():
    invalid_data = [{"amount": "NaN", "category": 123, "notes": None}]
    response = test_client.post("/expenses/2024-08-16", json=invalid_data)
    assert response.status_code == 422 

def test_analytics():
    response = test_client.post("/analytics/", json={"start_date": "2024-08-01", "end_date": "2024-08-31"})
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)

def test_analytics_invalid_date():
    response = test_client.post("/analytics/", json={"start_date": "invalid", "end_date": "invalid"})
    assert response.status_code == 422  
