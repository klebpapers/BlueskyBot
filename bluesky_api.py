from atproto import Client
import os

BLUESKY_HANDLE = os.getenv("BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

if not BLUESKY_HANDLE or not BSKY_APP_PASSWORD:
    raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD environment variables")

client = Client()
client.login(BLUESKY_HANDLE, BSKY_APP_PASSWORD)

MAX_POST_LENGTH = 300

async def post_to_bluesky(paper):
    title = paper["title"]
    doi = paper.get("doi")

    if not doi:
        print("Skipping (no DOI):", title)
        return

    doi_url = f"https://doi.org/{doi}"

    # Leave room for link and newline
    max_title_len = MAX_POST_LENGTH - len(doi_url) - 1
    if len(title) > max_title_len:
        title = title[:max_title_len - 3] + "..."

    post = f"{title}\n{doi_url}"
    client.send_post(text=post)
    print("✅ Posted:", post)
