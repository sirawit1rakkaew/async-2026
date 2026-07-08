# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently and awaiting them individually without gather.
import asyncio
from time import ctime, time

async def cook_spaghetti(customer):
    print(f"{ctime()} -> starting to cook spaghetti for {customer} ")
    await asyncio.sleep(1)
    print(f"{ctime()} -> finished cooking spaghetti for {customer} ")
    
async def main():
    start_time = time()
 
    task_a = asyncio.create_task(cook_spaghetti("A"))
    task_b = asyncio.create_task(cook_spaghetti("B"))
    
   
    await task_a
    await task_b
    
    
    print(f"total time: {time() - start_time:.2f} seconds")
    
if __name__ == "__main__":
        asyncio.run(main())