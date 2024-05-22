from datetime import date

from fastapi.testclient import TestClient

from backend.main import app

from backend.schema import *




# def test_get_chats_success():
#     client = TestClient(app)
#     response = client.get("/chats")
#     data = response.json()

#     assert response.status_code == 200
#     assert "meta" in data
#     assert "count" in data["meta"]
#     assert "chats" in data
#     assert isinstance(data["chats"], list)
#     #check if chats are sorted by name
#     if len(data["chats"]) > 1:
#         assert data["chats"][0]['name'] <= data["chats"][1]['name']

# def test_get_chat_with_id_success():
#     client = TestClient(app)
#     chat_id = "6215e6864e884132baa01f7f972400e2"  # Replace with an ID of a chat known to exist
#     response = client.get(f"/chats/{chat_id}")
#     data = response.json()

#     assert response.status_code == 200
#     assert "chat" in data
#     assert data["chat"]["id"] == chat_id
#     # Add additional assertions here to validate the structure and data of the returned chat

# def test_get_chat_with_id_failure():
#     client = TestClient(app)
#     chat_id = "fakeid"  # Use an ID that does not exist
#     response = client.get(f"/chats/{chat_id}")
#     data = response.json()

#     assert response.status_code == 404
#     assert data["detail"]["type"] == "entity_not_found"
#     assert data["detail"]["entity_name"] == "Chat"
#     assert data["detail"]["entity_id"] == chat_id


def test_get_chats_success(client):
    response = client.get("/chats")
    data = response.json()

    assert response.status_code == 200
    assert "meta" in data
    assert "count" in data["meta"]
    assert "chats" in data
    assert isinstance(data["chats"], list)
    # Check if chats are sorted by name
    if len(data["chats"]) > 1:
        assert data["chats"][0]['name'] <= data["chats"][1]['name']

def test_get_chat_with_id_success(client):
    chat_id = "6215e6864e884132baa01f7f972400e2"  # Replace with an ID of a chat known to exist
    response = client.get(f"/chats/{chat_id}")
    data = response.json()

    assert response.status_code == 200
    assert "chat" in data
    assert data["chat"]["id"] == chat_id
    # Add additional assertions here to validate the structure and data of the returned chat

def test_get_chat_with_id_failure(client):
    chat_id = "fakeid"  # Use an ID that does not exist
    response = client.get(f"/chats/{chat_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["type"] == "entity_not_found"
    assert data["detail"]["entity_name"] == "Chat"
    assert data["detail"]["entity_id"] == chat_id



def test_update_chat_name():
    chat_id = "6ad56d52b138432a9bba609533015cf3"
    update_params = {"name": "updated chat name"}
    expected_chat = {
        "id": chat_id,
        "name": update_params["name"],
        "user_ids": ["doolittle", "talby"],
        "owner_id": "doolittle",
        "created_at": "2023-06-19T23:51:59"
    }
    client = TestClient(app)
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}

    # test that the update is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}


def test_update_chat_invalid_id():
    chat_id = "invalid_id"
    update_params = {"name": "updated chat name"}
    client = TestClient(app)
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_delete_chat():
    chat_id = "6ad56d52b138432a9bba609533015cf3"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    assert response.content == b""

    # test that the delete is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

def test_delete_chat_invalid_id():
    chat_id = "invalid_id"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }

def test_get_chat_messages_success():
    client = TestClient(app)
    chat_id = "6215e6864e884132baa01f7f972400e2"
    response = client.get(f"/chats/{chat_id}/messages")
    data = response.json()

    assert response.status_code == 200
    assert "meta" in data
    assert "count" in data["meta"]
    assert "messages" in data
    assert isinstance(data["messages"], list)

def test_get_chat_messages_invalid_chat_id():
    client = TestClient(app)
    chat_id = "fakeid"  # Replace with an ID of a chat known not to exist
    response = client.get(f"/chats/{chat_id}/messages")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["type"] == "entity_not_found"
    assert data["detail"]["entity_name"] == "Chat"
    assert data["detail"]["entity_id"] == chat_id

def test_get_chat_users_success():
    client = TestClient(app)
    chat_id = "6215e6864e884132baa01f7f972400e2"  # Replace with an ID of a chat known to have users
    response = client.get(f"/chats/{chat_id}/users")
    data = response.json()

    assert response.status_code == 200
    assert "meta" in data
    assert "count" in data["meta"]
    assert "users" in data
    assert isinstance(data["users"], list)


def test_get_chat_users_chat_not_found():
    client = TestClient(app)
    chat_id = "fakeid" 
    response = client.get(f"/chats/{chat_id}/users")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["type"] == "entity_not_found"
    assert data["detail"]["entity_name"] == "Chat"
    assert data["detail"]["entity_id"] == chat_id

