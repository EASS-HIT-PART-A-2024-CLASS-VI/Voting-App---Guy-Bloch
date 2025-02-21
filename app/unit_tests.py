import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app


@pytest.mark.asyncio
async def test_add_candidate():
    async with AsyncClient(base_url="http://backend:8000") as client:
        # Create a new candidate
        response = await client.post("/candidates/", json={"name": "Alice"})
        data = response.json()
        candidate_id = data["id"]

        # Assert that the candidate is added
        assert response.status_code == 200
        assert data["name"] == "Alice"
        assert data["votes"] == 0
        assert "id" in data  # Make sure the id is returned

        # Cleanup: Delete the candidate after the test
        await client.delete(f"/candidates/{candidate_id}")


@pytest.mark.asyncio
async def test_list_candidates():
    async with AsyncClient(base_url="http://backend:8000") as client:
        # List candidates (this should include the one we added)
        response = await client.get("/candidates/")

        # Assert the response is successful
        assert response.status_code == 200
        candidates = response.json()
        assert isinstance(candidates, list)
        assert len(candidates) > 0  # Ensure there is at least one candidate


@pytest.mark.asyncio
async def test_cast_vote():
    # First, add a candidate
    async with AsyncClient(base_url="http://backend:8000") as client:
        response = await client.post("/candidates/", json={"name": "Bob"})
        candidate = response.json()
        candidate_id = candidate["id"]

        # Cast a vote for the candidate
        response = await client.post("/vote/", json={"candidate_id": candidate_id})
        assert response.status_code == 200
        assert response.json() == {"message": "Vote cast successfully"}

        # Verify the vote count
        response = await client.get("/candidates/")
        candidates = response.json()
        bob_candidate = next(c for c in candidates if c["id"] == candidate_id)
        assert bob_candidate["votes"] == 1  # Ensure the vote was counted

        # Cleanup: Delete the candidate after the test
        await client.delete(f"/candidates/{candidate_id}")


@pytest.mark.asyncio
async def test_delete_candidate():
    # First, add a candidate
    async with AsyncClient(base_url="http://backend:8000") as client:
        response = await client.post("/candidates/", json={"name": "Charlie"})
        candidate = response.json()
        candidate_id = candidate["id"]

        # Delete the candidate
        response = await client.delete(f"/candidates/{candidate_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Candidate deleted successfully"}

        # Verify the candidate is no longer in the list
        response = await client.get("/candidates/")
        candidates = response.json()
        assert not any(c["id"] == candidate_id for c in candidates)


@pytest.mark.asyncio
async def test_get_results():
    # Clear the candidates collection before the test to ensure a clean state
    async with AsyncClient(base_url="http://backend:8000") as client:
        await client.delete("/candidates/")  # Add an endpoint or manually delete from DB

    # Add candidates and cast some votes
    async with AsyncClient(base_url="http://backend:8000") as client:
        response = await client.post("/candidates/", json={"name": "Dave"})
        candidate_dave = response.json()
        candidate_id_dave = candidate_dave["id"]

        response = await client.post("/candidates/", json={"name": "Eve"})
        candidate_eve = response.json()
        candidate_id_eve = candidate_eve["id"]

        # Cast votes
        await client.post("/vote/", json={"candidate_id": candidate_id_dave})
        await client.post("/vote/", json={"candidate_id": candidate_id_dave})
        await client.post("/vote/", json={"candidate_id": candidate_id_eve})

        # Get results
        response = await client.get("/results/")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0  # Check if results are returned

        # Ensure both Dave and Eve are in the results
        assert any(c["name"] == "Dave" for c in results)
        assert any(c["name"] == "Eve" for c in results)

        # Cleanup: Delete the candidates after the test
        await client.delete(f"/candidates/{candidate_id_dave}")
        await client.delete(f"/candidates/{candidate_id_eve}")
