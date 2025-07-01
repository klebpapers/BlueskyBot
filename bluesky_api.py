from atproto import Client
import os
import aiohttp
import asyncio

BLUESKY_HANDLE = os.getenv("BSKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")
TLY_API_KEY = os.getenv("TLY_API_KEY")  # You must set this in GitHub secrets or locally

if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
    raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD environment variables")

client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

async def shorten_url(url):
    if not TLY_API_KEY:
        return url  # Fallback to original if no key
    async with aiohttp.ClientSession() as session:
        async with session.post("https://t.ly/api/v1/link/shorten", json={
            "long_url": url,
            "domain": "https://t.ly",
        }, headers={"Content-Type": "application/json", "Authorization": f"Bearer {TLY_API_KEY}"}) as resp:
            data = await resp.json()
            return data.get("short_url", url)

def truncate(text, max_length):
    return text if len(text) <= max_length else text[:max_length - 1] + "…"

async def post_to_bluesky(paper):
    short_link = await shorten_url(paper["link"])
    base_content = f"{paper['title']}\n{short_link}"
    content = truncate(base_content, 300)

    print(f"Posting to Bluesky: {content}")
    client.send_post(text=content)

