import feedparser
import json
import hashlib
from datetime import datetime, timedelta
from scheduler import schedule_posts
from pathlib import Path

FEEDS_FILE = "feeds.txt"
DB_FILE = "posted_db.json"

def load_feeds():
    with open(FEEDS_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def load_db():
    if not Path(DB_FILE).exists():
        return set()
    with open(DB_FILE, "r") as f:
        return set(json.load(f))

def save_db(posted_ids):
    with open(DB_FILE, "w") as f:
        json.dump(list(posted_ids), f)

def generate_id(entry):
    return hashlib.md5(entry.title.encode("utf-8")).hexdigest()

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

    save_posted_db(posted_ids)  # ✅ This should be at the same level as `return`
    return new_papers

if __name__ == "__main__":
    papers = fetch_new_papers()
    if papers:
        schedule_posts(papers)
