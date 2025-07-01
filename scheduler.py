import asyncio
from bluesky_api import post_to_bluesky

def schedule_posts(papers):
    asyncio.run(schedule_async(papers))

async def schedule_async(papers):
    interval = (23 * 3600) / len(papers)
    for i, paper in enumerate(papers):
        await asyncio.sleep(interval * i)
        await post_to_bluesky(paper["title"], paper["link"])
