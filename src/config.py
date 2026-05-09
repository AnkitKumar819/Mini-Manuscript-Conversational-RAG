# src/config.py

# =========================
# DATA PATHS
# =========================

IMAGE_DIR = "data/images"

OCR_OUTPUT_DIR = "output/ocr"

CHROMA_DB_DIR = "chroma_db"


# =========================
# CHUNK SETTINGS
# =========================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 50


# =========================
# EMBEDDING MODEL
# =========================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# =========================
# OPENAI MODEL
# =========================

LLM_MODEL = "gpt-4o-mini"


# =========================
# RETRIEVAL
# =========================

TOP_K = 3
