# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.
import asyncio
from time import ctime, time

async def kitchen_crew():
    print(f"{ctime()} -> [Chef] puts noodles in the pot")
    await asyncio.sleep(1)
    print(f"{ctime()} -> [Chef] takes noodles out of the pot")
    
async def bar_crew():
    print(f"{ctime()} -> [Bar] puts ice in the glass")
    await asyncio.sleep(1)
    print(f"{ctime()} -> [Bar] takes ice out of the glass")

async def main():
    task_kitchen = asyncio.create_task(kitchen_crew())
    task_bar = asyncio.create_task(bar_crew())

  

    await task_kitchen
    await task_bar


if __name__ == "__main__":
    asyncio.run(main())