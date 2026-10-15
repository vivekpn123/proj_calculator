import pytest
from app import app

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize(("a", "b", "op", "expected"), [
    (8, 2, "add", 10),
    (8, 2, "subtract", 6),
    (8, 2, "multiply", 16),
    (8, 2, "divide", 4),
    (-3, 2, "add", -1),
])
def test_calculations(client, a, b, op, expected):
    response = client.post("/calculate", json={"a": a, "b": b, "op": op})
    assert response.status_code == 200
    assert response.get_json()["result"] == expected

def test_divide_by_zero(client):
    response = client.post("/calculate", json={"a": 8, "b": 0, "op": "divide"})
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.get_json()["error"]

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Colourful Calculator" in response.data
