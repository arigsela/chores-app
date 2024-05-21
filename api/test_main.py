from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_chore():
    response = client.post(
        "/chores",
        json={"name": "Test Chore", "points": 10},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Chore"
    assert response.json()["points"] == 10

def test_read_chores():
    response = client.get("/chores", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_chore():
    # Create a chore associated with the created kid
    chore_data = {"name": "Test Chore", "points": 10}
    chore_response = client.post("/chores", json=chore_data, headers={"Authorization": "Bearer test_token"})
    chore_id = chore_response.json()["id"]

    # Read the chore
    response = client.get(f"/chores/{chore_id}", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["id"] == chore_id
    assert response.json()["name"] == "Test Chore"
    assert response.json()["points"] == 10

def test_update_chore():
    # Create a kid with the specified kid_id
    kid_data = {"name": "Test Kid"}
    kid_response = client.post("/kids", json=kid_data, headers={"Authorization": "Bearer test_token"})
    kid_id = kid_response.json()["id"]
    
    # Create a chore associated with the created kid
    chore_data = {"name": "Test Chore", "points": 10, "kid_id": kid_id}
    chore_response = client.post("/chores", json=chore_data, headers={"Authorization": "Bearer test_token"})
    chore_id = chore_response.json()["id"]
    
    # Update the chore
    updated_chore_data = {"name": "Updated Chore", "points": 20, "kid_id": kid_id}
    response = client.put(
        f"/chores/{chore_id}",
        json=updated_chore_data,
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Chore"
    assert response.json()["points"] == 20
    assert response.json()["kid_id"] == kid_id

def test_delete_chore():
    # Create a kid for the chore
    kid_data = {"name": "Test Kid"}
    kid_response = client.post("/kids", json=kid_data, headers={"Authorization": "Bearer test_token"})
    kid_id = kid_response.json()["id"]

    # Create a chore associated with the created kid
    chore_data = {"name": "Test Chore", "points": 10, "kid_id": kid_id}
    chore_response = client.post("/chores", json=chore_data, headers={"Authorization": "Bearer test_token"})
    chore_id = chore_response.json()["id"]

    # Delete the chore
    response = client.delete(f"/chores/{chore_id}", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "Chore deleted successfully"

def test_create_reward():
    reward_data = {"name": "Test Reward", "points": 50}
    response = client.post(
        "/rewards",
        json=reward_data,
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Reward"
    assert response.json()["points"] == 50

def test_award_reward_to_kid():
    # Create a kid
    kid_data = {"name": "Test Kid"}
    kid_response = client.post("/kids", json=kid_data, headers={"Authorization": "Bearer test_token"})
    kid_id = kid_response.json()["id"]

    # Create a reward
    reward_data = {"name": "Test Reward", "points": 50}
    reward_response = client.post("/rewards", json=reward_data, headers={"Authorization": "Bearer test_token"})
    reward_id = reward_response.json()["id"]

    # Award the reward to the kid
    response = client.post(
        f"/kids/{kid_id}/rewards",
        params={"reward_id": reward_id},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["kid_id"] == kid_id
    assert response.json()["reward_id"] == reward_id

def test_read_rewards():
    response = client.get("/rewards", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_kid():
    response = client.post(
        "/kids",
        json={"name": "Test Kid"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Kid"

def test_read_kids():
    response = client.get("/kids", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
