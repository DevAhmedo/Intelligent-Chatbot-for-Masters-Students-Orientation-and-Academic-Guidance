# Intelligent-Chatbot-for-Masters-Students-Orientation-and-Academic-Guidance

A chatbot for masters students' orientation and academic guidance using RAG (Retrieval-Augmented Generation).

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama** (for the LLM):
   - Download from [ollama.ai](https://ollama.ai)
   - Pull the required models:
     ```bash
     ollama pull llama3
     ollama pull nomic-embed-text
     ```

3. **Populate the database**:
   ```bash
   python populate_database.py
   ```
   This creates the `chroma_db` folder with vector embeddings from the PDFs in `data/`.

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Files

- `app.py`: Streamlit web app
- `query_data.py`: RAG query logic
- `populate_database.py`: Script to build the vector database
- `data/`: Source PDF documents
- `chroma_db/`: Vector database (generated, not in repo)