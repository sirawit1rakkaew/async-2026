# foodcourt_02_gather.py
import asyncio
from time import ctime, perf_counter
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301018"
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")

    start = perf_counter()

    # 1. Create 3 orders from different shops (they will run concurrently).
    chicken_order = send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice")
    noodle_order = send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
    steak_order = send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak")

    # 2. Use gather to run all orders concurrently and wait for ALL of them to finish.
    results = await asyncio.gather(chicken_order, noodle_order, steak_order)

    # 3. Serve every dish once they are all ready.
    for result in results:
        print(f"{ctime()} | [Pickup] Shop: {result['shop']} | Menu: {result['menu']} is ready!")

    elapsed = perf_counter() - start
    print(f"{ctime()} | Total time: {elapsed:.2f} seconds (Equals to the slowest dish).")

if __name__ == "__main__":
    asyncio.run(main())
