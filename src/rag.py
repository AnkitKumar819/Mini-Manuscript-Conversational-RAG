# src/rag.py

import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

from langchain_openai import ChatOpenAI

import base64
from langchain_core.messages import HumanMessage
from langchain_community.callbacks import get_openai_callback

from chunking import load_ocr_documents
from chunking import split_documents

from config import EMBEDDING_MODEL
from config import CHROMA_DB_DIR
from config import LLM_MODEL
from config import TOP_K


# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()


# =========================
# EMBEDDING MODEL
# =========================

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# =========================
# CREATE OR LOAD VECTOR DB
# =========================

def get_vector_db():

    # Check if DB already exists
    if os.path.exists(CHROMA_DB_DIR):

        print("Loading existing ChromaDB...")

        vector_db = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embedding_model
        )

    else:

        print("Creating new ChromaDB...")

        documents = load_ocr_documents()
        
        if not documents:
            raise ValueError("No documents found in output/ocr! Please run src/ocr.py first on your images.")

        chunks = split_documents(documents)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=CHROMA_DB_DIR
        )

        print("ChromaDB created successfully.")

    return vector_db


# =========================
# LOAD VECTOR DB
# =========================

vector_db = get_vector_db()


# =========================
# RETRIEVER
# =========================

retriever = vector_db.as_retriever(
    search_kwargs={"k": TOP_K}
)


# =========================
# OPENAI MODEL
# =========================

llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0
)


# =========================
# QA CHAIN
# =========================

# Simple RAG implementation without deprecated RetrievalQA

def ask_question(query):
    
    # Retrieve relevant documents
    docs = retriever.invoke(query)
    
    # Build context from retrieved documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Build prompt
    prompt = f"""You are a helpful manuscript assistant.

Use ONLY the provided context to answer the question.

If the answer is not available in the context, say:
"I could not find relevant information in the manuscript."

Context:
{context}

Question:
{query}

Answer:"""
    
    # Get response from LLM and track token usage
    with get_openai_callback() as cb:
        message = llm.invoke(prompt)
        tokens = cb.total_tokens
    
    answer = message.content if hasattr(message, 'content') else str(message)
    
    # Extract only necessary source info to avoid showing unwanted metadata
    sources = [f"Page {doc.metadata.get('page', 'Unknown')} of {doc.metadata.get('source', 'Unknown')}" for doc in docs]
    
    return answer, sources, tokens

# =========================
# IMAGE TRANSLATION
# =========================

def translate_image(image_bytes, target_language):
    
    # Encode the image to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Construct prompt
    prompt = f"Please identify the Sanskrit text in this manuscript image. Then, translate its meaning into {target_language}. Provide the original Sanskrit text (if legible) followed by the translation."
    
    # Construct the multimodal message
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]
    )
    
    # Get response from LLM and track token usage
    with get_openai_callback() as cb:
        response = llm.invoke([message])
        tokens = cb.total_tokens
        
    answer = response.content if hasattr(response, 'content') else str(response)
    
    return answer, tokens
