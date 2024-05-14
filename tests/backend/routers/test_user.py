from datetime import date

from fastapi.testclient import TestClient

from backend.main import app

#   response model = UserCollection
#   User specification 1 test (def get_users)
def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_get_all_users_sorted_by_created_at():
    client = TestClient(app)
    response = client.get("/users?sort=created_at")
    assert response.status_code == 200
    
    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["created_at"])


#   POST / "" / response_model = UserResponse
#   User specification 2 test (def get_user(user_id: str) )
def test_create_user():
    #   params to send
    create_params = {
    "id": "mingyu"
    }
    
    client = TestClient(app)
    response = client.post("/users", json=create_params)
    assert response.status_code == 200
    user = response.json()
    print(user["user"]["id"])
    #   response's id and getting user information should be same
    for key, value in create_params.items():
        assert user["user"][key] == value
        

#   User specification 2 invalid case (duplicate id)
def test_invalid_id():
    create_params = {
    "id": "mingyu"
    }
    
    client = TestClient(app)
    response = client.post("/users", json=create_params)
    #   reqeust same user id one more time
    response = client.post("/users", json=create_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": "mingyu"
        },
    }

#   User specification 3     
def test_get_user_by_id():
    user_id = "bishop"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    
    expected_response = { "id": "bishop", 
                         "created_at": "2014-04-14T10:49:07" }
    assert user["user"] == expected_response

    # invalid case
    
    expected_response ={
    "detail": {
        "type": "entity_not_found",
        "entity_name": "User",
        "entity_id": "none"
        }
    }
    
    user_id = "none"
    response = client.get(f"users/{user_id}")
    assert response.status_code == 404
    assert response.json() == expected_response
    
#   User specification 4
def test_user_chats_by_id():
    client = TestClient(app)
    user_id = "bishop"
    response = client.get(f"users/{user_id}/chats")
    print(response)
    
    meta = response.json()["meta"]
    
    expected_response = [{'id': '734eeb9ddaec43b2ab6e289a0d472376', 
                          'name': 'nostromo', 
                          'user_ids': ['bishop', 'burke', 'ripley'], 
                          'owner_id': 'ripley', 
                          'created_at': '2023-09-18T14:18:46'}]
    
    assert response.status_code == 200
    assert meta["count"] == len(response.json()["chats"])
    assert response.json()["chats"] == expected_response
    
    #   invalid case
    user_id = "none"
    response = client.get(f"users/{user_id}/chats")
    
    expected_response= {
    "detail": {
        "type": "entity_not_found",
        "entity_name": "User",
        "entity_id": "none"
    }
    }
    assert response.status_code == 404
    assert response.json() == expected_response

#==============Chat specification==============

def test_get_chats():
    client = TestClient(app)
    response = client.get("chats")
    print(response)
    
    #   count of chats
    meta = response.json()["meta"]
    #   sorted by name
    chats = response.json()["chats"]
    
    assert response.status_code == 200
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_chat_by_id():
    client = TestClient(app)
    chat_id = "6215e6864e884132baa01f7f972400e2"
    response = client.get(f"chats/{chat_id}")
    
    assert response.status_code == 200
    
    expected_response = {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": "skynet",
        "user_ids": ["sarah", "terminator"],
        "owner_id": "sarah",
        "created_at": "2023-07-08T18:46:47"
    }
    assert response.json()["chat"] == expected_response
    
    #   another chat
    chat_id = "660c7a6bc1324e4488cafabc59529c93"
    response = client.get(f"chats/{chat_id}")
    
    assert response.status_code == 200
    
    expected_response = {
        "id": "660c7a6bc1324e4488cafabc59529c93",
        "name": "terminators",
        "user_ids": ["reese", "sarah"],
        "owner_id": "reese",
        "created_at": "2023-04-12T20:11:21"
    }
    assert response.json()["chat"] == expected_response

def test_get_chat_by_invalid_id():
    
    client = TestClient(app)
    chat_id = "123456789"
    response = client.get(f"chats/{chat_id}")
    
    expected_error_response = {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }        
    }
    assert response.status_code == 404
    assert response.json() == expected_error_response
    
def test_update_chat_by_given_id():
    client = TestClient(app)
    update_name = "mingyu chat"
    body_request = {
        "name": update_name
    }
    chat_id = "6215e6864e884132baa01f7f972400e2"
    
    response = client.put(f"/chats/{chat_id}", json=body_request)
    
    assert  response.status_code == 200
    
    expected_response = {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": update_name,
        "user_ids": ["sarah", "terminator"],
        "owner_id": "sarah",
        "created_at": "2023-07-08T18:46:47"
    }
    assert response.json()["chat"] == expected_response
    
def test_update_chat_invlid_id():
    client = TestClient(app)
    chat_id = "123456"
    body_request = {
        "name": "not valid"
    }
    
    error_response = {
    "detail": {
        "type": "entity_not_found",
        "entity_name": "Chat",
        "entity_id": chat_id
        }   
    }

    response = client.put(f"/chats/{chat_id}", json = body_request)
    
    assert response.status_code == 404
    assert response.json() == error_response

def test_delete_chat():
    client = TestClient(app)
    chat_id = "36b18c30f5eb4c7888229474d12e426f"
    response = client.delete(f"chats/{chat_id}")
    assert response.status_code == 204

def test_delete_chat_invalid_id():
    client = TestClient(app)
    chat_id = "123456"
    response = client.delete(f"chats/{chat_id}")
    error_response = {
        "detail": {
        "type": "entity_not_found",
        "entity_name": "Chat",
        "entity_id": chat_id
        }
    }
    assert response.status_code == 404
    assert response.json() == error_response

def test_get_chat_list():
    client = TestClient(app)
    chat_id = "734eeb9ddaec43b2ab6e289a0d472376"
    response = client.get(f"chats/{chat_id}/messages")
    
    assert response.status_code == 200
    
    meta =  response.json()["meta"]
    messages = response.json()["messages"]    
    
    assert meta["count"] == len(response.json()["messages"])
    assert messages == sorted(messages, key=lambda message: message["created_at"])
    
def test_get_chat_list_invalid_id():
    client = TestClient(app)
    chat_id = "123456"
    response = client.get(f"chats/{chat_id}/messages")
    
    assert response.status_code == 404
    
    error_response = {
        "detail": {
        "type": "entity_not_found",
        "entity_name": "Chat",
        "entity_id": chat_id
        }
    }
    assert response.json() == error_response

def test_get_user_in_chat():
    client = TestClient(app)
    chat_id = "6215e6864e884132baa01f7f972400e2"
    
    response = client.get(f"chats/{chat_id}/users")
    meta = response.json()["meta"]
    users = response.json()["users"]
    
    #   it has to response with sarah, and terminator
    print(response)
    expect_response = [
        {
            "id": "sarah",
            "created_at": "2006-03-02T22:30:11"
        },
        {
            "id": "terminator",
            "created_at": "2014-04-05T21:45:39"
        }
    ]
    assert response.status_code == 200
    assert meta["count"] == len(users)
    assert users == expect_response
    
def test_get_user_in_chat_invalid_id():
    client = TestClient(app)
    chat_id = "123456"
    
    response = client.get(f"chats/{chat_id}/users")
    
    error_response = {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
    }
    
    assert response.status_code == 404
    assert response.json() == error_response