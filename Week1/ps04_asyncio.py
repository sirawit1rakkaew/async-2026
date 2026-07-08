from time import ctime, time, process_time
import asyncio
import os
import threading
import psutil

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    await asyncio.sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ
    print(f"Finished making coffee for {customer_name} at {ctime()}")

async def main():
    customers = ["Alice", "Bob", "Charlie"]
    tasks = [make_coffee(customer) for customer in customers]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    