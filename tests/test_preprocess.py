import pytest
from src.preprocessing.preprocess import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_preprocess():
    response = client.post("/preprocess", json={
        "product_id": "123",
        "unit_price": 100.0,
        "comp_1": 95.0,
        "comp_2": 97.0,
        "comp_3": 93.0,
        "qty": 50,
        "product_category_name": "Electronics",
        "product_score": 4.5,
        "volume": 100.0,
        "lag_price": 98.0
    })
    assert response.status_code == 200
    assert response.json()["product_id"] == "123"
    assert "price_gap" in response.json()