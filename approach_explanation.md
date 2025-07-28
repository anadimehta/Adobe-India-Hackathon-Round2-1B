# Approach Explanation

## Overview

This project is designed to automate the extraction and semantic analysis of PDF documents for Challenge 1B. The workflow processes collections of PDFs, extracts structured outlines, and generates JSON outputs suitable for downstream tasks such as information retrieval or further NLP analysis.

## Modular Structure

The codebase is organized into modular components for clarity and maintainability:

- **parser.py**: Main entry point for processing PDF collections. Handles CLI arguments, orchestrates the workflow, and manages input/output.
- **src/text_utils.py**: Contains text cleaning and normalization utilities to ensure consistent processing of extracted text.
- **src/embedding.py**: Provides functions to generate text embeddings using a local or specified model, enabling semantic search capabilities.
- **src/chroma_db.py**: Manages document chunking, embedding storage, and similarity search using ChromaDB.
- **src/main.py**: Implements the main semantic search pipeline, integrating all modules and handling input/output specifications.

## Processing Pipeline

1. **Input Handling**  
   The system accepts either a single collection or all collections in a specified directory. Each collection contains a JSON configuration and a set of PDF documents.

2. **PDF Outline Extraction**  
   For each PDF, the system uses `pymupdf4llm` to convert pages to markdown. It then parses the markdown to extract hierarchical outlines (titles, sections, subsections) using regular expressions and normalization utilities.

3. **Text Cleaning**  
   Extracted text is cleaned to remove artifacts such as ligatures, special punctuation, markdown formatting, and redundant whitespace, ensuring high-quality input for downstream processing.

4. **Document Chunking and Embedding**  
   Documents are split into manageable chunks. Each chunk is embedded using a fast local embedding model (via `fastembed`), enabling efficient semantic similarity search.

5. **ChromaDB Integration**  
   Chunks and their embeddings are stored in a ChromaDB instance, allowing for fast retrieval of relevant sections based on semantic similarity to a given query.

6. **Semantic Search and Output Generation**  
   For each query (from the input spec), the system retrieves the most relevant document sections, formats the results, and outputs a structured JSON file containing metadata, extracted sections, and analysis.

## Usage

- **Dockerized Execution**:  
  The project includes a Dockerfile for reproducible, environment-independent execution. Build and run the container to process collections and generate outputs.

- **Command-Line Interface**:  
  The user can process all collections or a specific collection using CLI flags:
  ```
  python parser.py --all
  python parser.py --collection "Collection 1"
  ```

## Key Features

- **Robust PDF Parsing**: Handles a variety of PDF layouts and extracts structured outlines.
- **Text Normalization**: Ensures clean, consistent text for analysis.
- **Semantic Search**: Uses local embeddings and vector search for efficient information retrieval.
- **Modular Design**: Facilitates maintenance, testing, and future extension.