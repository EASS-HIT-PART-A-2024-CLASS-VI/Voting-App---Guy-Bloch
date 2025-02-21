from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager
import os


# MongoDB Configuration

MONGO_URI = os.getenv("TEST_MONGO_URI","mongodb://mongo:27017/my_database")
DATABASE_NAME = os.getenv("TEST_DATABASE_NAME","voting_db")
COLLECTION_NAME = os.getenv("TEST_COLLECTION_NAME", "candidates")

client = None
db = None
candidates_collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, candidates_collection
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    candidates_collection = db[COLLECTION_NAME]
    yield  # This allows FastAPI to run the app
    client.close()

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Candidate(BaseModel):
    id: str = Field(..., description="The unique identifier for the candidate")
    name: str = Field(..., description="The name of the candidate")
    votes: int = Field(default=0, description="The number of votes the candidate has received")

class CandidateCreate(BaseModel):
    name: str

class Vote(BaseModel):
    candidate_id: str

class CandidateResult(Candidate):
    percentage: float = Field(..., description="The percentage of total votes the candidate has received")

# Add Candidate
@app.post("/candidates/", response_model=Candidate)
async def add_candidate(candidate: CandidateCreate):
    try:
        new_candidate = {"name": candidate.name, "votes": 0}
        result = await candidates_collection.insert_one(new_candidate)
        return Candidate(id=str(result.inserted_id), name=candidate.name, votes=0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add candidate: {str(e)}")

# List Candidates
@app.get("/candidates/", response_model=List[Candidate])
async def list_candidates():
    candidates = await candidates_collection.find().to_list(None)
    return [Candidate(id=str(c["_id"]), name=c["name"], votes=c["votes"]) for c in candidates]

# Cast Vote
@app.post("/vote/")
async def cast_vote(vote: Vote):
    if not ObjectId.is_valid(vote.candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate ID")

    candidate = await candidates_collection.find_one({"_id": ObjectId(vote.candidate_id)})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    await candidates_collection.update_one(
        {"_id": ObjectId(vote.candidate_id)},
        {"$inc": {"votes": 1}}
    )
    return {"message": "Vote cast successfully"}

# Delete Candidate
@app.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: str):
    if not ObjectId.is_valid(candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate ID")

    result = await candidates_collection.delete_one({"_id": ObjectId(candidate_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {"message": "Candidate deleted successfully"}

# Get Results
@app.get("/results/", response_model=List[CandidateResult])
async def get_results():
    candidates = await candidates_collection.find().to_list(None)
    total_votes = sum(c["votes"] for c in candidates)

    if total_votes == 0:
        return [
            CandidateResult(id=str(c["_id"]), name=c["name"], votes=c["votes"], percentage=0.0)
            for c in candidates
        ]

    results = [
        CandidateResult(
            id=str(c["_id"]),
            name=c["name"],
            votes=c["votes"],
            percentage=round((c["votes"] / total_votes) * 100, 2)
        )
        for c in candidates
    ]

    # Sort by votes in descending order
    results.sort(key=lambda x: x.votes, reverse=True)
    return results