# Program 5: Sequential Execution (The Wrong Way)
# Concept: Showing that simply awaiting one after another is still sequential (Synchronous behavior).
import asyncio
from time import ctime, time

async def serve_customer(name):
    print(f"{ctime()} -> cooking for {name} ")
    await asyncio.sleep(1)
    print(f"{ctime()} -> served for {name} ")
    
async def main():
    start_time = time()
    await serve_customer("A")
    await serve_customer("B")
    
    
    print(f"total time: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
            
