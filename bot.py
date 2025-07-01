import os
import random
import feedparser
from atproto import Client
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

BSKY_HANDLE = os.getenv('BSKY_HANDLE')
BSKY_APP_PASSWORD = os.getenv('BSKY_APP_PASSWORD')

FEEDS_FILE = 'feeds.txt'
POSTED_FILE = 'posted_links.txt'


def load_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def save_line(path, line):
    with open(path, 'a') as f:
        f.write(line + '\n')


def fetch_new(feeds, posted):
    items = []
    for url in feeds:
        f = feedparser.parse(url)
        for e in f.entries:
            link = e.link.strip()
            if link not in posted:
                title = e.title.strip()
                text = f"{title}\n{link}"
                items.append((link, text))
    return items


def post_to_bsky(text):
    client = Client()
    client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)
    client.send_post(text=text)
    print("✅ Posted:", text)


def main():
    feeds = load_lines(FEEDS_FILE)
    posted = set(load_lines(POSTED_FILE))
    new = fetch_new(feeds, posted)

    if not new:
        print("No new articles.")
        return

    link, text = random.choice(new)
    post_to_bsky(text)
    save_line(POSTED_FILE, link)


if __name__ == '__main__':
    main()
