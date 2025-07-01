from atproto import Client
import os
import aiohttp
import asyncio

BLUESKY_HANDLE = os.getenv("BSKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
    raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD environment variables")

client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)


def truncate(text, max_length):
    return text if len(text) <= max_length else text[:max_length - 1] + "…"

async def post_to_bluesky(paper):
    doi_url = f"https://doi.org/{paper['doi']}" if paper.get("doi") else paper["link"]
    short_link = await shorten_url(doi_url)
    base_content = f"{paper['title']}\n{short_link}"
    content = truncate(base_content, 300)

    print(f"Posting to Bluesky: {content}")
    client.send_post(text=content)

