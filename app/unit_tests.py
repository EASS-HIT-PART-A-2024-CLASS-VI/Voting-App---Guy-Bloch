import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize the test client
client = TestClient(app)


def test_add_candidate():
    """Test adding a new candidate."""
    response = client.post("/candidates/", json={"name": "Alice"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Alice"
    assert response.json()["votes"] == 0


def test_list_candidates():
    """Test listing all candidates."""
    response = client.get("/candidates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_cast_vote():
    """Test casting a vote for a candidate."""
    # Add a candidate first
    candidate_response = client.post("/candidates/", json={"name": "Bob"})
    candidate_id = candidate_response.json()["id"]

    # Cast a vote
    vote_response = client.post("/vote/", json={"candidate_id": candidate_id})
    assert vote_response.status_code == 200
    assert vote_response.json()["message"] == "Vote cast successfully"

    # Verify the vote count
    results_response = client.get("/results/")
    assert results_response.status_code == 200
    for candidate in results_response.json():
        if candidate["id"] == candidate_id:
            assert candidate["votes"] == 1
            break
    else:
        pytest.fail("Candidate not found in results")


def test_results():
    """Test retrieving voting results."""
    response = client.get("/results/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_candidate():
    """Test deleting a candidate."""
    # Add a candidate first
    candidate_response = client.post("/candidates/", json={"name": "Charlie"})
    candidate_id = candidate_response.json()["id"]

    # Delete the candidate
    delete_response = client.delete(f"/candidates/{candidate_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Candidate deleted successfully"

    # Verify deletion
    candidates_response = client.get("/candidates/")
    assert candidates_response.status_code == 200
    assert all(candidate["id"] != candidate_id for candidate in candidates_response.json())
