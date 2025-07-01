from atproto import Client

BLUESKY_HANDLE = "klebpapers.bsky.social"
BLUESKY_APP_PASSWORD = "Ges08132001*15235"

client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

async def post_to_bluesky(title, link):
    post = f"{title}\n{link}"
    client.send_post(text=post)
