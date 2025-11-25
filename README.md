# Apache Jira Scraper & Transformer Pipeline

## Overview

This project builds a reliable, fault-tolerant, and scalable data pipeline that scrapes issue data from Apache Jira projects and transforms it into a structured JSONL dataset suitable for training Large Language Models (LLMs). It is designed to demonstrate robust data engineering practices, including error handling, modularity, and clean data output.

## Features

* ✅ Scrapes issues, metadata, comments from three Apache Jira projects: **HADOOP**, **SPARK**, **KAFKA**
* ✅ Graceful handling of pagination, rate limits, empty/malformed responses
* ✅ Transforms raw issues into LLM-friendly JSONL with summaries, category classification, and Q&A pairs
* ✅ Includes recovery, fault-tolerance, and modular design
* ✅ Output ready for downstream NLP training or analysis

## Directory Structure

```
jira-scraper-assignment/
├── analysis/
│   └── llm_enhance.py         # Adds summary, category, Q&A via OpenAI API
├── output/
│   ├── clean_issues.jsonl     # Cleaned raw issues
│   ├── final_dataset.jsonl    # LLM-enhanced output
│   ├── HADOOP_raw.jsonl       # Raw data per project
│   ├── KAFKA_raw.jsonl
│   └── SPARK_raw.jsonl
├── state/                    # Checkpointing for resume logic (if implemented)
├── clean.py                  # Cleans raw to structured
├── config.json               # Config for scraper
├── scraper.py                # Fetches issues using Jira API
├── transform.py              # Extracts essential fields
├── requirements.txt
├── README.md                 # This file
└── set_api_key.ps1           # Helper script for setting OpenAI key (Windows)
```

## Setup Instructions

1. **Clone this repository**:

```bash
git clone https://github.com/your-username/jira-scraper-assignment.git
cd jira-scraper-assignment
```

2. **Create & activate virtual environment (optional but recommended)**:

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
.\venv\Scripts\activate         # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set OpenAI API Key** (for LLM-enhancement step):

```powershell
# For current session (PowerShell)
$env:OPENAI_API_KEY = "your_real_key_here"

# Or run helper script
.\set_api_key.ps1 "your_real_key_here"
```

## Usage

### 1. Scrape Apache Jira Issues

```bash
python scraper.py
```

Output: `output/{PROJECT}_raw.jsonl` files

### 2. Clean and Normalize Raw Data

```bash
python clean.py
```

Output: `output/clean_issues.jsonl`

### 3. Transform with OpenAI (adds summaries, Q&A)

```bash
python analysis/llm_enhance.py
```

Output: `output/final_dataset.jsonl`

## Sample Input/Output

**Input Snippet (clean_issues.jsonl)**:

```json
{
  "project": "SPARK",
  "issue_key": "SPARK-492",
  "title": "Add unit tests for shuffle operations",
  "description": "Need to add these in the shuffle branch.",
  "comments": ["Github comment from mateiz: Unit tests for shuffle operations."]
}
```

**Transformed Output (final_dataset.jsonl)**:

```json
{
  "summary": "Added unit tests to validate shuffle logic...",
  "category": "Improvement",
  "qna": [
    {"question": "Why were shuffle operation tests added?", "answer": "To ensure correctness..."},
    ...
  ]
}
```

## Edge Cases Handled

* Missing fields or comments → handled with defaults
* HTTP 429 or API errors → printed/logged, script fails gracefully
* Duplicate entries avoided during LLM enhancement (resumable logic)
* Folder auto-creation for outputs

## Future Enhancements

* Async scraping for speed
* Retry logic/backoff on API failures
* Configurable pagination batch sizes
* Logging and CLI for project-level control
* Add test cases and CI hooks

## Authors

* Assignment completed by: **VIJAYAGEETHA V**
* For: **Scaler SDE Internship (2026 Batch)**


