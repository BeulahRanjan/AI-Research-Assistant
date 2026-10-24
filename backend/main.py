
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import documents, health, research


app = FastAPI(
    title="AI Research Assistant API",
    description="Research over PDFs using retrieval-augmented generation.",
    version="0.1.0",
)

 app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

 app.include_router(health.router)
# app.include_router(documents.router)
# app.include_router(research.router)


@app.get("/")
def home():
    return {
        "message": "AI Research Assistant API is running!"
    }
