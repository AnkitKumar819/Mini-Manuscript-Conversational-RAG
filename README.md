# 📜 Mini Manuscript RAG ✨

A production-ready Retrieval-Augmented Generation (RAG) system designed to interact with and translate manuscript documents.

## 🚀 Features
- **Conversational RAG**: Ask questions about the manuscript contents.
- **Multi-modal Translation**: Upload images of Sanskrit manuscripts and get meanings in English or Hindi.
- **Premium UI**: Interactive dark-themed Streamlit interface with animated backgrounds and glassmorphism.
- **Token Tracking**: Real-time monitoring of OpenAI token usage.

## 🛠️ Tech Stack
- **Backend**: Python, LangChain, OpenAI (GPT-4o-mini)
- **Vector Store**: ChromaDB
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Frontend**: Streamlit
- **OCR**: EasyOCR (for pre-processing)

## 📋 Setup Instructions

### 1. Prerequisites
- Python 3.10+
- OpenAI API Key

### 2. Fast Run (Windows)
Simply double-click the `run.bat` file. It will:
- Create a virtual environment.
- Install all dependencies.
- Ask you to provide your OpenAI API key in the `.env` file if it's missing.
- Launch the Streamlit application.

### 3. Manual Setup
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd manuscript-rag
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment**:
   - Create a `.env` file in the root directory.
   - Add your key: `OPENAI_API_KEY=your_key_here`
5. **Run the Application**:
   ```bash
   streamlit run src/streamlit_app.py
   ```

## 🖼️ Project Structure
- `src/`: Core logic and Streamlit app.
- `data/`: Raw manuscript images.
- `output/`: Processed OCR texts.
- `chroma_db/`: Local vector database.

