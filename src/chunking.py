# Chunking logic for texts
# src/chunking.py

import os

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import Document

from config import OCR_OUTPUT_DIR
from config import CHUNK_SIZE
from config import CHUNK_OVERLAP

from utils import get_page_number


# ======================================
# LOAD OCR DOCUMENTS
# ======================================

def load_ocr_documents():

    documents = []

    text_files = sorted(
        os.listdir(OCR_OUTPUT_DIR)
    )

    for file in text_files:

        file_path = os.path.join(
            OCR_OUTPUT_DIR,
            file
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        page_number = get_page_number(file)

        doc = Document(
            page_content=text,
            metadata={
                "page": page_number,
                "source": "manuscript"
            }
        )

        documents.append(doc)

    return documents


# ======================================
# SPLIT DOCUMENTS INTO CHUNKS
# ======================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    docs = load_ocr_documents()

    chunks = split_documents(docs)

    print(f"Documents: {len(docs)}")

    print(f"Chunks: {len(chunks)}")

    print("\nSample Chunk:\n")

    print(chunks[0].page_content)

    print("\nMetadata:\n")

    print(chunks[0].metadata)