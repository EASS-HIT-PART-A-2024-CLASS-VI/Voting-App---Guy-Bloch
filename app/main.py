from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to make requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Data Models
class Candidate(BaseModel):
    id: str
    name: str
    votes: int = 0

class CandidateCreate(BaseModel):
    name: str

class Vote(BaseModel):
    candidate_id: str

class CandidateResult(BaseModel):
    id: str
    name: str
    votes: int
    percentage: float

# In-Memory Database
candidates = {}


@app.post("/candidates/", response_model=Candidate)
def add_candidate(candidate: CandidateCreate):
    candidate_id = str(uuid4())
    new_candidate = Candidate(id=candidate_id, name=candidate.name, votes=0)
    candidates[candidate_id] = new_candidate
    return new_candidate


@app.get("/candidates/", response_model=List[Candidate])
def list_candidates():
    return list(candidates.values())


@app.post("/vote/")
def cast_vote(vote: Vote):
    if not vote.candidate_id:
        raise HTTPException(status_code=422, detail="candidate_id is required")

    if vote.candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidates[vote.candidate_id].votes += 1
    return {"message": "Vote cast successfully"}


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: str):
    if candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")
    del candidates[candidate_id]
    return {"message": "Candidate deleted successfully"}


@app.get("/results/", response_model=List[CandidateResult])
def get_results():
    total_votes = sum(candidate.votes for candidate in candidates.values())
    if total_votes == 0:
        return [
            CandidateResult(
                id=candidate.id,
                name=candidate.name,
                votes=candidate.votes,
                percentage=0.0
            )
            for candidate in candidates.values()
        ]
    return [
        CandidateResult(
            id=candidate.id,
            name=candidate.name,
            votes=candidate.votes,
            percentage=round((candidate.votes / total_votes) * 100, 2)
        )
        for candidate in sorted(candidates.values(), key=lambda x: x.votes, reverse=True)
    ]
