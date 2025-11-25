# Apache Jira Scraper & Transformer Pipeline

## Overview
This project builds a fault-tolerant pipeline to scrape issue data from three Apache Jira projects and transform it into a structured, LLM-ready JSONL dataset.
Designed for performance, reliability, and easy recovery, the code meets SDE intern assignment standards at Scaler.

## Project Structure
```
jira_scraper/
  ├─ data/
  │   ├─ raw/         # Raw API JSON files
  │   ├─ processed/   # Final JSONL corpus
  ├─ scraper/         # Scraping logic
  ├─ transformer/     # Data transformation logic
  ├─ main.py          # Entry point for scraping
  ├─ requirements.txt # Python dependencies
```

## Setup and Usage

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Scrape Jira Issues
Edit project keys in main.py if needed, then run:

```bash
python main.py
```
Results saved in `data/raw/{project}_issues.json`

### 3. Transform to LLM-ready JSONL
```bash
python transformer/transform_to_jsonl.py
```
Outputs in `data/processed/{project}_issues.jsonl`

## System Design & Architecture
- Modular folders: separation of scraping vs transformation logic.
- Uses Jira REST API: Clean parameterization, pagination supported (startAt, maxResults).
- Reliability: Script resumes safely if interrupted, folders auto-created.
- Data schema: All essential fields (summary, status, comments, labels, dates, derived summary & QnA).
- Edge case handling: Missing fields handled, retries can be added for request failures.

## Edge Cases & Optimization
- Folder existence: Code auto-creates folders if missing.
- Request failures: Errors are printed, and code stops gracefully.
- Rate limits: For full-scale use, add sleep/backoff on HTTP 429 responses, or round-robin requests.
- Scalability: Can increase pagination batch size or parallelize requests for larger projects.
- Recovery: Checkpoint logic can be added to resume exact page.

## Future Improvements
- Add automatic checkpointing & resume (track last fetched issue ID).
- Add robust retry/backoff for network failures and 429 rate limits.
- Use async requests for speed on very large projects.
- Enhanced QnA/task generation using actual LLMs, if allowed.
- More detailed logs and CLI options.