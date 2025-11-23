import os
import json
from typing import Dict, Optional
from openai import OpenAI
from .prompts import get_extraction_prompt, SYSTEM_PROMPT

class LLMExtractor:
    """Handles LLM-based document and clause extraction"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI LLM client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPEN_AI_API_KEY"))
        self.model = "gpt-4o-mini"
    
    def extract_document_and_clauses(self, pdf_text: str) -> Dict:
        """
        Extract document metadata and clauses from PDF text using LLM.
        
        Args:
            pdf_text: Full text extracted from PDF
            
        Raises:
            Exception: If LLM API call fails or returns invalid JSON
            
        Returns:
            dict: Contains 'document' (metadata) and 'clauses' (list) keys
        """
        prompt = get_extraction_prompt(pdf_text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.0  # No temperature for deterministic extraction
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._validate_and_normalize(result)
            
        except Exception as e:
            raise Exception(f"LLM extraction failed: {str(e)}")
    

    
    def _validate_and_normalize(self, result: Dict) -> Dict:
        """
        Validate and normalize LLM response structure.
        
        Args:
            result: Raw response from LLM
            
        Returns:
            dict: Validated response with required fields and defaults
        """
        if 'document' not in result:
            result['document'] = {}

        document = result['document']
        document.setdefault('document_type', None)
        document.setdefault('effective_date', None)

        if 'clauses' not in result or not isinstance(result['clauses'], list):
            result['clauses'] = []

        validated_clauses = []
        for clause in result['clauses']:
            if isinstance(clause, dict):
                validated_clause = {
                    'clause_number': clause.get('clause_number'),
                    'heading': clause.get('heading'),
                    'clause_type': clause.get('clause_type'),
                    'start_page': self._safe_int(clause.get('start_page')),
                    'end_page': self._safe_int(clause.get('end_page'))
                }
                validated_clauses.append(validated_clause)
        
        result['clauses'] = validated_clauses
        return result
    
    def _safe_int(self, value) -> Optional[int]:
        """
        Safely convert value to integer.
        
        Args:
            value: Value to convert
            
        Returns:
            int or None: Integer if conversion succeeds, None otherwise
        """
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

def extract_with_llm(pdf_text: str) -> Dict:
    """
    Extract document structure using LLM (convenience function).
    
    Args:
        pdf_text: Full text extracted from PDF
        
    Raises:
        Exception: If LLM extraction fails
        
    Returns:
        dict: Contains 'document' and 'clauses' keys
    """
    extractor = LLMExtractor()
    return extractor.extract_document_and_clauses(pdf_text)