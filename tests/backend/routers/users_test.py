from fastapi.testclient import TestClient

from backend.main import app


def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

def test_get_users_sorted_by_id():
    client = TestClient(app)
    response = client.get("/users")
    data = response.json()

    assert response.status_code == 200
    assert "meta" in data
    assert "count" in data["meta"]
    assert "users" in data
    assert isinstance(data["users"], list)
    
    # Check if users are sorted by id
    if len(data["users"]) > 1:
        user_ids = [user["id"] for user in data["users"]]
        assert user_ids == sorted(user_ids), "Users are not sorted by id"


def test_create_user_success():
    client = TestClient(app)
    new_user_id = "new_user_id"
    response = client.post("/users", json={"id": new_user_id})
    data = response.json()

    assert response.status_code == 200
    assert data["user"]["id"] == new_user_id
    assert "created_at" in data["user"]

def test_create_user_duplicate_id():
    client = TestClient(app)
    existing_user_id = "existing_user_id"
    # First, create a user
    client.post("/users", json={"id": existing_user_id})

    # Then, try to create the same user again
    response = client.post("/users", json={"id": existing_user_id})
    data = response.json()

    assert response.status_code == 422
    assert data["detail"]["type"] == "duplicate_entity"
    assert data["detail"]["entity_name"] == "User"
    assert data["detail"]["entity_id"] == existing_user_id


def test_get_user_by_id():
    client = TestClient(app)
    user_id = "bomb20"
    expected_user = {
        "id": user_id,
        "created_at": "2022-03-21T08:30:02",
    }
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"user": expected_user}


def test_get_user_invalid_id():
    user_id = "notreal"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }

def test_get_user_chats_success():
    client = TestClient(app)
    user_id = "bomb20" 
    response = client.get(f"/users/{user_id}/chats")
    data = response.json()

    assert response.status_code == 200
    assert "meta" in data
    assert "count" in data["meta"]
    assert "chats" in data
    assert isinstance(data["chats"], list)


def test_get_user_chats_user_not_found():
    client = TestClient(app)
    user_id = "fakeid"
    response = client.get(f"/users/{user_id}/chats")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["type"] == "entity_not_found"
    assert data["detail"]["entity_name"] == "User"
    assert data["detail"]["entity_id"] == user_id

