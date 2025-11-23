#!/bin/bash

set -e

API_URL="http://localhost:8000"
PDF_FILE="./example-file.pdf"

echo "=========================================="
echo "LLM Extraction API Demo"
echo "=========================================="
echo ""

if [ ! -f "$PDF_FILE" ]; then
    echo "❌ Error: PDF file not found: $PDF_FILE"
    exit 1
fi

echo "🔍 Checking if API is running..."
if ! curl -s "$API_URL/" > /dev/null; then
    echo "❌ Error: API is not running at $API_URL"
    echo "   Please start the API with: docker-compose up"
    exit 1
fi
echo "✅ API is running"
echo ""

echo "📄 Step 1: Uploading and extracting PDF..."
echo "   File: $PDF_FILE"
echo ""

RESPONSE=$(curl -s -X POST "$API_URL/api/extract" \
    -F "file=@$PDF_FILE" \
    -H "accept: application/json")

DOCUMENT_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "")

if [ -z "$DOCUMENT_ID" ]; then
    echo ""
    echo "❌ Failed to extract document. Check the response:"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi

echo "✅ Document extracted successfully! ID: $DOCUMENT_ID"
echo ""
echo "=========================================="

echo ""
echo "📋 Step 2: Getting extraction by ID..."
echo "   Document ID: $DOCUMENT_ID"
echo ""

curl -s "$API_URL/api/extractions/$DOCUMENT_ID" | python3 -m json.tool

echo ""
echo "=========================================="

echo ""
echo "📚 Step 3: Listing all extractions..."
echo ""

curl -s "$API_URL/api/extractions" | python3 -m json.tool

echo ""
echo "=========================================="
echo "✅ Demo completed successfully!"
echo "=========================================="