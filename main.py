import os
import time
import json
import feedparser
from scheduler import schedule_posts

DB_FILE = "posted_ids.json"
FEED_FILE = "feeds.txt"

def load_posted_db():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r") as f:
        return set(json.load(f))

def save_posted_db(posted_ids):
    with open(DB_FILE, "w") as f:
        json.dump(list(posted_ids), f)

def fetch_new_papers():
    posted_ids = load_posted_db()
    new_papers = []

    with open(FEED_FILE, "r") as f:
        feeds = [line.strip() for line in f if line.strip()]

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            uid = entry.get("id") or entry.get("link") or entry.get("title")
            if uid not in posted_ids:
                doi = entry.get("dc_identifier") or entry.get("doi")
                if not doi and "doi.org" in entry.get("link", ""):
                    doi = entry["link"].split("doi.org/")[-1]

                new_papers.append({
                    "id": uid,
                    "title": entry.get("title"),
                    "doi": doi,
                    "link": entry.get("link"),
                    "summary": entry.get("summary", "")[:200]
                })
                posted_ids.add(uid)

    save_posted_db(posted_ids)
    return new_papers

if __name__ == "__main__":
    print("Fetching new papers...")
    papers = fetch_new_papers()

    if not papers:
        print("No new papers to post.")
    else:
        print(f"Found {len(papers)} new papers. Scheduling posts...")
        schedule_posts(papers)
