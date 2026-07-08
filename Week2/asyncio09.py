# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.
import asyncio
from time import ctime, time

async def serve_customer(name):
    print(f"{ctime()} -> cooking for {name} ")
    await asyncio.sleep(2)
    print(f"{ctime()} -> served for {name} ")
    
async def main():
    start_time = time()
    customers = ["A", "B", "C", "D"]
    tasks = []
    for name in customers:
        task = asyncio.create_task(serve_customer(name))
        tasks.append(task)
    
    for task in tasks:
        await task
    print(f"Served all {len(customers)} customers In {time() - start_time:.2f} seconds")
    
if __name__ == "__main__":
        asyncio.run(main())