import requests
import json
import os

os.makedirs("data/raw", exist_ok=True)

JIRA_API = "https://issues.apache.org/jira/rest/api/2/search"
PROJECT_KEYS = ["KAFKA", "HADOOP", "SPARK"]
MAX_RESULTS = 50
TOTAL_TO_FETCH = 100  # adjust as needed

def fetch_project_issues(project_key):
    all_issues = []
    start_at = 0

    print(f"Fetching issues for project: {project_key}")
    while len(all_issues) < TOTAL_TO_FETCH:
        params = {
            "jql": f"project={project_key}",
            "startAt": start_at,
            "maxResults": MAX_RESULTS,
            "fields": "summary,status,reporter,description,comment,priority,assignee,labels,created,updated"
        }
        resp = requests.get(JIRA_API, params=params)
        if resp.status_code != 200:
            print("Error fetching issues:", resp.status_code, resp.text)
            break
        data = resp.json()
        batch = data.get('issues', [])
        if not batch:
            break
        all_issues.extend(batch)
        start_at += MAX_RESULTS
        print(f"Fetched {len(all_issues)} of {TOTAL_TO_FETCH} issues so far for {project_key}...")
        if len(batch) < MAX_RESULTS:
            break

    # Save to file
    out_file = f"data/raw/{project_key.lower()}_issues.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"issues": all_issues}, f, indent=2)
    print(f"Saved {len(all_issues)} issues to {out_file}")
    for issue in all_issues[:5]:
        print("Issue:", issue["key"], "-", issue["fields"]["summary"])

if __name__ == "__main__":
    for key in PROJECT_KEYS:
        fetch_project_issues(key)
