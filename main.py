"""
main.py — FastAPI application for Study Buddy.

Endpoints:
- POST /study  : runs the 4-agent collaborative pipeline
- GET  /health : returns system status
- GET  /       : serves the web frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from pipeline import run_pipeline

app = FastAPI(
    title="Study Buddy",
    description="Multi-agent study assistant — notes + quiz generator",
    version="1.0.0",
)


class StudyRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="The topic to study (e.g. 'Photosynthesis', 'World War II')",
    )
    source_text: str | None = Field(
        default=None,
        description="Optional: paste chapter or lecture notes for text-mode extraction",
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=15,
        description="Number of practice quiz questions to generate",
    )


class StudyResponse(BaseModel):
    topic: str
    mode: str
    facts: str
    notes: str
    quiz: list[dict]
    review: dict
    attempts: int
    elapsed_seconds: float
    error: str | None = None


@app.post("/study", response_model=StudyResponse)
def study(req: StudyRequest):
    """Run the 4-agent pipeline and return notes + quiz."""
    result = run_pipeline(
        topic=req.topic,
        source_text=req.source_text,
        num_questions=req.num_questions,
    )
    if result.error and not result.notes:
        raise HTTPException(status_code=500, detail=result.error)
    return result.to_dict()


@app.get("/health")
def health():
    return {"status": "ok", "provider": "Groq"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")
