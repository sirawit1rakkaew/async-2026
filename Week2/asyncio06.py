# Program 6: Creating a Concurrent Task
# Concept: Wrapping a coroutine inside asyncio.create_task() to schedule it to run in the background.
import asyncio
from time import ctime, time

async def cook_spaghetti(customer):
    print(f"{ctime()} -> starting to cook spaghetti for {customer} ")
    await asyncio.sleep(1)
    print(f"{ctime()} -> finished cooking spaghetti for {customer} ")
    
async def main():
    start_time = time()
 
    task_a = asyncio.create_task(cook_spaghetti("A"))
    
    print(f"{ctime()} -> main progtam can do orther things while waiting for the task to finish")
  
   
    await task_a
    
    
    print(f"total time: {time() - start_time:.2f} seconds")
    
if __name__ == "__main__":
        asyncio.run(main())