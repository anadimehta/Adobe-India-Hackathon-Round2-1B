# Adobe-India-Hackathon-Round2-1B

# PDF Smart Semantic Search & Query Response

An intelligent PDF processing system that extracts structured outlines and metadata from PDF collections and provides semantic search capabilities for document analysis.

## Quick Start

```bash
git clone https://github.com/anadimehta/Adobe-India-Hackathon-Round2-1B.git
cd challenge1B
pip install -r requirements.txt
```

## Features

* Batch PDF processing across collections
* Extract structured titles, outlines, and hierarchy
* Semantic search with vector embeddings
* JSON output for integration and analysis
* Configurable input and output directories

## Project Structure

```
challenge1B/
├── llm4_to_json.py          # Main PDF processing script
├── process_all.sh           # Script to run batch PDF processing
├── semantic_search_all.sh   # Script for batch semantic search
├── example_input.json       # Template for input configuration
├── src/
│   └── semantic_search.py   # Core semantic search module
├── challenge_pdfs/          # Input PDF collections
├── challenge_outputs_json/  # Output directory for JSON results
└── requirements.txt         # Dependencies
```

## PDF Processing with `llm4_to_json.py`

### Process All Collections

```bash
python llm4_to_json.py --all
```

Processes all PDFs from all collection folders, extracting:

* Document outlines (H1–H3 hierarchy)
* Section titles and ranks
* Saves results in `challenge_outputs_json/`

### Process a Single Collection

```bash
python llm4_to_json.py --collection "Collection 1"
```

### Custom Input/Output Directories

```bash
python llm4_to_json.py --all --input-dir my_pdfs --output-dir my_output
```

### Help Options

```bash
python llm4_to_json.py --help
```

## Output Format

The output JSON contains metadata and structured content:

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip",
    "processing_timestamp": "2025-07-28T23:13:36.489538"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Main Topic",
      "importance_rank": 1,
      "page_number": 1
    }
  ]
}
```

## Input Configuration Template

Each collection needs a `challenge1b_input.json` file. Example:

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {
      "filename": "document.pdf",
      "title": "Document Title"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

## Semantic Search with `semantic_search.py`

Run semantic search across one or more collections:

### Process All Collections

```bash
python3 semantic_search.py "challenge_pdfs/Collection 1/challenge1b_input.json" "challenge_outputs_json/1.json" && \
python3 semantic_search.py "challenge_pdfs/Collection 2/challenge1b_input.json" "challenge_outputs_json/2.json" && \
python3 semantic_search.py "challenge_pdfs/Collection 3/challenge1b_input.json" "challenge_outputs_json/3.json"
```

### Individual Collection Example

```bash
python3 semantic_search.py "challenge_pdfs/Collection 2/challenge1b_input.json" "challenge_outputs_json/2.json"
```

### What It Does

* Generates vector embeddings for PDF chunks
* Uses ChromaDB for semantic similarity search
* Matches queries with top-ranked relevant sections

## Dependencies

* `pymupdf4llm`
* `fastembed`
* `langchain-chroma`
* `langchain-community`
* `langchain-text-splitters`

## Technical Pipeline

1. PDF Extraction using PyMuPDF
2. Heading Detection and structural parsing
3. Normalization for formatting and punctuation
4. Embedding for semantic representation
5. ChromaDB Search for similarity-based responses

## Contributing

1. Fork this repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature/my-feature`
5. Open a Pull Request

## Troubleshooting

* Missing PDFs: Make sure your collection folders have the required files
* Import errors: Run `pip install -r requirements.txt`
* Permission issues: Ensure write access to output folders

