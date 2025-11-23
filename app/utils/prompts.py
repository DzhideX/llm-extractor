SYSTEM_PROMPT = "You are an expert legal document analyzer. Extract document metadata and identify all clauses in the provided document. Return valid JSON only."

EXTRACTION_PROMPT_TEMPLATE = """
Analyze the following document and extract:

1. Document metadata:
   - title: The document title
   - document_type: Type of document (e.g., "Contract", "Agreement", "Policy", "Terms of Service")
   - effective_date: The effective date in YYYY-MM-DD format (if mentioned)

2. All clauses/sections with:
   - clause_number: The clause or section number (e.g., "1", "2.1", "3(a)")
   - heading: The clause title/heading
   - clause_type: Type of clause (e.g., "confidentiality", "payment", "termination", "liability", "definitions", "general")
   - start_page: Page number where clause starts
   - end_page: Page number where clause ends

DOCUMENT TEXT:
{pdf_text}

Return ONLY valid JSON in this exact format:
{{
    "document": {{
        "title": "Document Title",
        "document_type": "Contract",
        "effective_date": "2025-01-01"
    }},
    "clauses": [
        {{
            "clause_number": "1",
            "heading": "Definitions",
            "clause_type": "definitions",
            "start_page": 1,
            "end_page": 2
        }},
        {{
            "clause_number": "2",
            "heading": "Payment Terms",
            "clause_type": "payment",
            "start_page": 2,
            "end_page": 3
        }}
    ]
}}

If any field cannot be determined, use null. Ensure all page numbers are integers.
"""

def get_extraction_prompt(pdf_text: str) -> str:
    """
    Format extraction prompt with PDF text.
    
    Args:
        pdf_text: Full text extracted from PDF
        
    Returns:
        str: Formatted prompt for LLM
    """
    return EXTRACTION_PROMPT_TEMPLATE.format(pdf_text=pdf_text)