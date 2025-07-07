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

    interval = SECONDS_IN_6_HOURS / total
    print(f"📆 Spacing out {total} posts every {int(interval)} seconds.")

    for i, paper in enumerate(papers):
        delay = int(i * interval)
        print(f"⏳ Scheduled post {i+1}/{total} in {delay} seconds: {paper['title']}")
        asyncio.create_task(delayed_post(paper, delay))

    # Keep the event loop alive until all posts are done
    await asyncio.sleep(int(SECONDS_IN_6_HOURS + interval))

async def delayed_post(paper, delay):
    await asyncio.sleep(delay)
    await post_to_bluesky(paper)
