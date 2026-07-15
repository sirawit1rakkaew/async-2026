# foodcourt_05_mix_concepts.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301018"
    print(f"{ctime()} | --- [Task 5] Advanced Practice: Mixing concepts together ---")

    start = perf_counter()

    # 1. Order noodles with a standard waiting cycle (1.5s) wrapped as a Task.
    noodle_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
    )

    # 2. Order chicken rice (0.8s) but wrap it under a strict 1.0s timeout,
    #    then put that wait_for wrapper inside a create_task execution tree.
    chicken_task = asyncio.create_task(
        asyncio.wait_for(
            send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"),
            timeout=1.0
        )
    )

    try:
        # 3. Resolve both structures inside a single gather collection.
        results = await asyncio.gather(noodle_task, chicken_task)
        print(f"{ctime()} | Success: All food served on time! Received {len(results)} dishes.")
    except asyncio.TimeoutError:
        print(f"{ctime()} | Timeout occurred: One of the dishes took too long!")

    elapsed = perf_counter() - start
    print(f"{ctime()} | Total elapsed time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
