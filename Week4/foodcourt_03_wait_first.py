# foodcourt_03_wait_first.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301018"
    print(f"{ctime()} | --- [Task 3] Practice using wait (FIRST_COMPLETED) ---")

    start = perf_counter()

    # 1. Wrap all 3 orders as Task objects so they start running in the background.
    tasks = {
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Thigh")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")),
        asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")),
    }

    # 2. Race the tasks: return as soon as the FASTEST one is done.
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3. Pick up the winning dish (the first one that finished).
    winner = done.pop().result()
    print(f"{ctime()} | Winner served dish: Shop: {winner['shop']} | Menu: {winner['menu']}")

    # 4. Cancel every remaining pending order to free up resources.
    print(f"{ctime()} | Cleaning up: Canceling {len(pending)} remaining pending orders...")
    for task in pending:
        task.cancel()

    elapsed = perf_counter() - start
    print(f"{ctime()} | Total waiting time for the first dish: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
