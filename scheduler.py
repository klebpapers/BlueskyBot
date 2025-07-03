import asyncio
from bluesky_api import post_to_bluesky

SECONDS_IN_6_HOURS = 6 * 60 * 60  # 21,600 seconds

def schedule_posts(papers):
    asyncio.run(schedule_async(papers))

async def schedule_async(papers):
    total = len(papers)
    if total == 0:
        print("✅ No papers to post.")
        return
