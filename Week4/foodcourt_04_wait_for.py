# foodcourt_04_wait_for.py
import asyncio
from time import ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301018"
    print(f"{ctime()} | --- [Task 4] Practice using wait_for to handle timeouts ---")

    # Order a steak (usually 4.0s) but enforce a hard limit of 2.0 seconds.
    print(f"{ctime()} | [System] Order sent. Monitoring 2.0s timeout limit...")
    try:
        # 1. Wrap the order with wait_for and a strict 2.0s SLA.
        result = await asyncio.wait_for(
            send_order_to_kitchen(MY_STUDENT_ID, "steak", "T-Bone Steak"),
            timeout=2.0
        )
        # 2. If it finishes in time, serve the dish.
        print(f"{ctime()} | Served dish: Shop: {result['shop']} | Menu: {result['menu']}")
    except asyncio.TimeoutError:
        # 3. If it exceeds the limit, skip the meal and leave immediately.
        print(f"{ctime()} | Timeout occurred: Steak took too long! Leaving the food court now.")

if __name__ == "__main__":
    asyncio.run(main())
