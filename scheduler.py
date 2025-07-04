import asyncio
from bluesky_api import post_to_bluesky

SECONDS_IN_23_HOURS = 23 * 60 * 60

def schedule_posts(papers):
    asyncio.run(schedule_async(papers))

async def schedule_async(papers):
    total = len(papers)
    if total == 0:
        print("✅ No papers to post.")
        return

    interval = SECONDS_IN_23_HOURS / total
    print(f"📅 Scheduling {total} posts every {int(interval)} seconds.")

    for i, paper in enumerate(papers):
        delay = int(i * interval)
        asyncio.create_task(delayed_post(paper, delay))

    # Wait long enough for all posts to be made
    await asyncio.sleep(int(SECONDS_IN_23_HOURS + interval))

async def delayed_post(paper, delay):
    await asyncio.sleep(delay)
    await post_to_bluesky(paper)
