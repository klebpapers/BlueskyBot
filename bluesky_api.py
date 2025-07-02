from atproto import Client
import os

BLUESKY_HANDLE = os.getenv("BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

if not BLUESKY_HANDLE or not BSKY_APP_PASSWORD:
    raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD environment variables")

client = Client()
client.login(BLUESKY_HANDLE, BSKY_APP_PASSWORD)

async def post_to_bluesky(paper):
    title = paper["title"]
    doi = paper.get("doi")

    if not doi:
        print("No DOI found, skipping:", title)
        return

    doi_url = f"https://doi.org/{doi}"
    post = f"{title}\n{doi_url}"

    # Ensure the post is within Bluesky's 300-character limit
    if len(post) > 300:
        title = title[:295 - len(doi_url)] + "..."
        post = f"{title}\n{doi_url}"

    client.send_post(text=post)
    print("✅ Posted:", title)

