"""
Phase 1 -- hardcoded extraction, using Groq for the LLM call.

Reads a PDF, pulls out its raw text, and asks a Groq-hosted model to extract
a FIXED set of fields (defined below in FIELDS_SCHEMA), returned as clean JSON.

This is deliberately hardcoded. Phase 2 will make the field list dynamic --
this step is just to prove the core pipeline (PDF -> text -> LLM -> JSON) works.

Usage:
    python scripts/extract.py sample_data/sample_invoice.pdf
"""

import sys
import json
import os

import pdfplumber
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROG_API_KEY"))

# A solid general-purpose model on Groq's free tier. Swap to another model
# name from console.groq.com/docs/models if you want to compare quality/speed.
MODEL = "openai/gpt-oss-20b"

# The fixed schema for Phase 1. In Phase 2, this gets built dynamically
# from whatever fields the user defines.
FIELDS_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "extracted_fields",
        "schema": {
            "type": "object",
            "properties": {
                "sender_name": {
                    "type": ["string", "null"],
                    "description": "The name of the person or company issuing the document.",
                },
                "date": {
                    "type": ["string", "null"],
                    "description": "The date on the document, in YYYY-MM-DD format if possible.",
                },
                "total_amount": {
                    "type": ["number", "null"],
                    "description": "The final total amount due, as a plain number with no currency symbol.",
                },
                "currency":{
                    "type": ["string","null"],
                    "description":"the currency of the total amount, e.g. USD, EUR, ILS."
                }
            },
            "required": ["sender_name", "date", "total_amount","currency"],
            "additionalProperties": False,
        },
    },
}


def extract_text_from_pdf(path: str) -> str:
    """Pull raw text out of every page of a PDF."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
    return "\n".join(pages)


def extract_fields(document_text: str) -> dict:
    """Send document text to Groq and force a structured JSON response."""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You extract structured data from documents. "
                            "Return only fields that match the given schema.",
            },
            {
                "role": "user",
                "content": f"Extract the fields from this document:\n\n{document_text}",
            },
        ],
        response_format=FIELDS_SCHEMA,
    )
    raw = completion.choices[0].message.content
    return json.loads(raw)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/extract.py <path-to-pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print("No extractable text found. This PDF may be scanned/image-based --")
        print("that case needs OCR, which is a later phase.")
        sys.exit(1)

    result = extract_fields(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
