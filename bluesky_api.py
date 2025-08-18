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
    link = paper.get("link")

    # Prefer DOI if available, else fall back to link
    if doi:
        doi = doi.strip()
        if doi.lower().startswith("doi:"):
            doi = doi[4:].strip()
        url = f"https://doi.org/{doi}"
    elif link:
        url = link.strip()
    else:
        print("⏭️ Skipping (no DOI or link):", title)
        return

    # Truncate title if needed
    max_title_len = MAX_POST_LENGTH - len(url) - 2
    if len(title) > max_title_len:
        title = title[:max_title_len - 3] + "..."

    post_text = f"{title}\n{url}"

    # Make link clickable with facets
    try:
        start = post_text.index(url)
        end = start + len(url)
        facets = [
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=url)],
                index=models.AppBskyRichtextFacet.ByteSlice(byteStart=start, byteEnd=end),
            )
        ]
    except ValueError:
        facets = []

    client.send_post(text=post_text, facets=facets)
    print("✅ Posted:", post_text)
