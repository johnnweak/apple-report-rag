# Apple Annual Report RAG System

A production-style RAG (Retrieval Augmented Generation) pipeline that lets you ask natural language questions about Apple's 2023 Annual Report and get answers with page citations.

## What I Built
- Ingested an 80-page PDF and chunked it into 91 overlapping segments
- Generated 1536-dimension embeddings using OpenAI's text-embedding-3-small
- Stored vectors in a persistent ChromaDB vector store
- Built semantic retrieval that finds the 3 most relevant chunks per question
- Wrapped everything in a Streamlit UI with conversation history and page citations

## Tech Stack
Python, OpenAI API, ChromaDB, Streamlit, PyPDF

## Known Limitations
Page citations reflect chunk start position due to 50-word overlap. Financial tables may extract inconsistently with pypdf — production solution would use pdfplumber.

## How to Run
1. Clone the repo
2. Add your OpenAI API key to a .env file
3. Run the ingestion notebook: analysis.ipynb
4. Launch the app: streamlit run app.py
