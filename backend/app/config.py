
import os
from pathlib import Path

from dotenv import load_dotenv

# Locate the backend directory.
BACKEND_DIR = Path(__file__).resolve().parents[1]

# Load environment variables from backend/.env.
load_dotenv(BACKEND_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Persistent vector database location.
CHROMA_PATH = BACKEND_DIR / "chroma_db"

# Folder for uploaded research papers.
UPLOAD_DIR = BACKEND_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
