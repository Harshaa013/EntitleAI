from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from eligibility_engine import find_eligible_schemes

app = FastAPI(
    title="EntitleAI Eligibility Engine",
    description="AI-based government scheme eligibility inference service",
    version="1.0"
)


class UserProfile(BaseModel):
    age: int
    income: int
    category: str
    occupation: str


@app.get("/")
def root():
    return {"message": "EntitleAI Eligibility Engine is running"}


@app.post("/check-eligibility")
def check_eligibility(user: UserProfile):
    user_data: Dict = user.dict()
    results = find_eligible_schemes(user_data)

    return {
        "eligible_schemes": results,
        "count": len(results)
    }
