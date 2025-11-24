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

## Extra

In this section, I go over my design decisions/tradeoffs, what I'd improve over time and any assumptions I made along the way of implementing this project:

### Improve with time:
- I would figure out a way to minimize the amount of text I need to send for the LLM to parse based on the business use case. Currently, we’re sending the whole text, but we could use a mixture of some heuristics to extract more relevant parts rather than sending all of it.
- Would take more care in what kind of error messages are being returned (based on whether this is a client facing or internal feature) in the API.
- Any kind of auth has been disregarded due to time constraints.
- Add caching on the /extract endpoint via redis for previously extracted documents (we could use hash-based deduplication for this).
- Add retry logic for transient LLM failures (we could use exponental backoff).
- Add a proper suite of tests, logging, track metrics. Also, code-wise, I'd add linting and formatting.


### Assumptions:
- The PDFs are legal documents with clauses. It would make sense to maybe have a cheap LLM call to catch whether or not the pdf is that, and then return a response asking a legal document to be sent.
- Assumed the PDFs wouldn’t be arbitrarily long. In case of pdfs with thousands of pages, we might have to think about more aggressive ways to figure out which parts of text are relevant to send to the LLM (the less we send the better ~ if performance is unchanged). However, even this would eventually not be enough. In that case, we would have to make multiple calls to the LLM rather than one singular file. We might want to cap the size of the PDF being sent as well (this depends on the business use case).