import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parents[1]
    PROJECT_ROOT = BASE_DIR.parent
    load_dotenv(PROJECT_ROOT / ".env")
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

#api metadata
APP_TITLE = "ResumeLens"
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = "using nlp(bert) to check resume for ATS"

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:8000"
]

#file
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
MAX_FILE_SIZE_MB = MAX_FILE_SIZE_BYTES / (1024 * 1024)  # Convert to MB

SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}

SPACY_MODEL_PRIMARY = "en_core_web_md"
SPACY_MODEL_SECONDARY = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

JD_KEYWORD_WEIGHT = float(os.getenv("JD_KEYWORD_WEIGHT", 0.65))
JD_SEMANTIC_WEIGHT = float(os.getenv("JD_SEMANTIC_WEIGHT", 0.35))

SCORE_WEIGHTS = {
    "formatting": 20,
    "keyword": 25,
    "content" :25,
    "skill_validation": 15,
    "ats_compatibility": 15,
}

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
