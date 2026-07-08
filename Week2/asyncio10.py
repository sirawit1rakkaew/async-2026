# Program 10: Extracting Return Values from Tasks
# Concept: Accessing returned results from completed Task objects using .result() or direct assignment.
import asyncio

async def calculate_bil(customer, base_price):
    print(f"Calculating bill for {customer}...")
    await asyncio.sleep(1)
    total = base_price * 1.07  # Adding tax
    return total
    
async def main():
    task_a = asyncio.create_task(calculate_bil("A", 100))
    task_b = asyncio.create_task(calculate_bil("B", 200))
    
    total_a = await task_a
    total_b = await task_b
    
    print(f"Total bill for A: ${total_a:.2f}")
    print(f"Total bill for B: ${total_b:.2f}")
    print(f"Combined total: ${total_a + total_b:.2f}")

if __name__ == "__main__":
    asyncio.run(main())