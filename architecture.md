# 🏗️ System Architecture

## 🔄 System Flow
The following diagram illustrates the end-to-end data pipeline of the Manuscript RAG system:

```text
[ Manuscript Images ]
       |
       | (Preprocessing: Grayscale + Gaussian Blur + Otsu Thresholding)
       v
[ EasyOCR (san, hi, en) ] ----> [ Raw Text Files ]
                                      |
                                      | (Recursive Character Splitting)
                                      v
[ HuggingFace Embeddings ] <--- [ Text Chunks ]
       | (all-MiniLM-L6-v2)
       v
[ ChromaDB (Local Store) ]
       |
       | (Similarity Search)
       v
[ Context Retrieval ] --------> [ GPT-4o-mini ]
                                      |
                                      | (Prompt Augmentation)
                                      v
                                [ Chat Interface ]
```

## 🛠️ Component Rationale

### 1. OCR: EasyOCR over Tesseract
We chose **EasyOCR** for this project because:
- **Indic Script Support**: It natively handles Devanagari (Sanskrit/Hindi) significantly better than Tesseract's default LSTM models without extensive custom training.
- **Deep Learning Native**: Built on PyTorch, providing better accuracy for stylized or aged manuscript text.

### 2. LLM: GPT-4o-mini
- **Cost-Efficiency**: High performance for RAG tasks at a fraction of the cost of GPT-4o.
- **Vision Support**: Enables the "Translate Image" feature without needing a separate model.

### 3. Chunking Strategy
- **Logic**: Used `RecursiveCharacterTextSplitter` with a **Chunk Size of 500** and **Overlap of 50**.
- **Rationale**: Manuscript pages often contain dense philosophical verses (Shlokas). A 500-character window is large enough to capture complete verses, while the 50-character overlap ensures that context transitions between chunks are not lost.

## 📈 Scaling Strategy (Production Readiness)

To scale this system for thousands of manuscripts, we would implement:
1.  **Distributed OCR Workers**: Move OCR processing to async workers (Celery/Redis) to handle batch uploads without blocking the UI.
2.  **Vector DB Sharding**: Migrate from local ChromaDB to a managed service like **Pinecone** or **Milvus** to support sharding and high-concurrency retrieval.
3.  **Embedding Caching**: Implement a Redis cache for common queries to avoid redundant embedding calculations and LLM calls.
4.  **CDN for Images**: Store raw manuscript images in an S3 bucket served via CloudFront (CDN) to ensure fast loading for global users.
5.  **Batch Ingestion**: Use a streaming pipeline (e.g., Kafka) to ingest and process new manuscript images as they are digitized.

