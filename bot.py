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
    feeds = load_feeds()
    posted_ids = load_db()
    new_papers = []

    for url in feeds:
        d = feedparser.parse(url)
        for entry in d.entries:
            paper_id = generate_id(entry)
            if paper_id not in posted_ids:
                new_papers.append({
                    "id": paper_id,
                    "title": entry.title,
                    "link": entry.link
                })
                posted_ids.add(paper_id)

    save_db(posted_ids)
    return new_papers

if __name__ == "__main__":
    papers = fetch_new_papers()
    if papers:
        schedule_posts(papers)
