import json
import os

RAW_DIR = "data/raw"
PROC_DIR = "data/processed"
os.makedirs(PROC_DIR, exist_ok=True)

PROJECTS = ["kafka", "hadoop", "spark"]
def fake_summarize(description):
    # Simple fake summary: first sentence or first 80 chars
    if not description:
        return ""
    return description.split(".")[0][:80]

def fake_generate_qna(issue):
    # Very basic QnA from issue fields
    qna = []
    qna.append({"question": "What is the issue title?", "answer": issue.get("summary", "")})
    qna.append({"question": "Who reported this issue?", "answer": issue.get("reporter", {}).get("displayName", "")})
    return qna

def extract_issue_fields(issue, project):
    fields = issue["fields"]
    comments = fields.get("comment", {}).get("comments", [])
    desc = fields.get("description", "")
    return {
        "key": issue.get("key", ""),
        "project": project.upper(),
        "title": fields.get("summary", ""),
        "status": fields.get("status", {}).get("name", ""),
        "reporter": fields.get("reporter", {}).get("displayName", ""),
        "created": fields.get("created", ""),
        "description": desc,
        "comments": [c.get("body", "") for c in comments],
        "labels": fields.get("labels", []),
        "summary": fake_summarize(desc),
        "qna": fake_generate_qna(fields)
    }


def transform_to_jsonl(project):
    raw_file = f"{RAW_DIR}/{project}_issues.json"
    proc_file = f"{PROC_DIR}/{project}_issues.jsonl"
    with open(raw_file, "r", encoding="utf-8") as rf, open(proc_file, "w", encoding="utf-8") as pf:
        data = json.load(rf)
        issues = data.get("issues", [])
        for issue in issues:
            row = extract_issue_fields(issue, project)
            pf.write(json.dumps(row) + "\n")
    print(f"Saved {len(issues)} issues to {proc_file}")

if __name__ == "__main__":
    for p in PROJECTS:
        transform_to_jsonl(p)
