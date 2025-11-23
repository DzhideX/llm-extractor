# LLM Extraction API

A FastAPI-based service that uses Large Language Models (LLMs) to automatically extract and structure information from PDF documents. The API analyzes legal and business documents, identifying key metadata and clauses with their locations.

## Features

- 📄 **PDF Text Extraction**: Automatically extracts text from PDF files with page markers
- 🤖 **AI-Powered Analysis**: Uses OpenAI's GPT models to identify document structure
- 📊 **Structured Output**: Returns document metadata and clauses in a structured format
- 💾 **Persistent Storage**: Stores extractions in SQLite database
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 🔍 **REST API**: Simple HTTP endpoints for extraction and retrieval

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd llm-extraction

# Create .env file with your OpenAI API key
echo "OPEN_AI_API_KEY=sk-proj-your-api-key-here" > .env
```

### 2. Build and Run

```bash
# Build the service
docker compose build

# Start the service (detached)
docker compose up -d

# Stop the service
docker compose down
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Extract Document from PDF

Upload a PDF file and extract its structure using AI.

**Endpoint:** `POST /api/extract`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/extract" \
  -H "accept: application/json" \
  -F "file=@demo/example-file.pdf"
```


### 2. Get Extraction by ID

Retrieve a specific document extraction with all its clauses.

**Endpoint:** `GET /api/extractions/{document_id}`

**Request:**
```bash
# Replace {document_id} with the actual ID (e.g., 1)
curl -X GET "http://localhost:8000/api/extractions/1" \
  -H "accept: application/json"
```

### 3. List All Extractions

Retrieve all document extractions with pagination support.

**Endpoint:** `GET /api/extractions`

**Request:**
```bash
# Get all extractions (default: first 100)
curl -X GET "http://localhost:8000/api/extractions" \
  -H "accept: application/json"

# With pagination parameters
curl -X GET "http://localhost:8000/api/extractions?offset=0&limit=10" \
  -H "accept: application/json"
```

**Query Parameters:**
- `offset` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

## Running the Demo

A demo script is provided to test all endpoints:

```bash
# Make the script executable
chmod +x demo/run_demo.sh

# Run the demo
cd demo
./run_demo.sh
```

The demo script will:
1. Upload `example-file.pdf` to the extraction API
2. Retrieve the extraction by ID
3. List all extractions in the database


## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PyMuPDF**: PDF text extraction
- **OpenAI API**: LLM-powered document analysis
- **SQLite**: Lightweight database
- **Docker**: Containerization