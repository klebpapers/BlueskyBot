from atproto import Client

BLUESKY_HANDLE = "klebpapers.bsky.social"
BLUESKY_APP_PASSWORD = "Ges08132001*15235"

client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

def truncate(text, max_length):
    return text if len(text) <= max_length else text[:max_length - 1] + "…"

async def post_to_bluesky(paper):
    # Compose the post content
    content = f"{paper['title']}\n{paper['link']}"

    # Enforce 300-character (grapheme) limit
    content = truncate(content, 300)

    print(f"Posting to Bluesky: {content}")
    client.send_post(text=content)
