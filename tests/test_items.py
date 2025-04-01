from .base_test import client


def test_create_item(client):
    response = client.post(
        "/v1/items/",
        json={"name": "test", "description": "test", "price": 1.0},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "test",
        "description": "test",
        "price": 1.0,
    }


def test_get_items(client):
    client.post(
        "/v1/items/",
        json={"name": "test", "description": "test", "price": 1.0},
    )

    response = client.get("/v1/items/")

    assert response.status_code == 200
    items = response.json()

    assert isinstance(items, list)
    assert len(items) > 0
    assert items[0]["name"] == "test"
    assert items[0]["description"] == "test"
    assert items[0]["price"] == 1.0
