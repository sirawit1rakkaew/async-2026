from time import ctime, time
import asyncio

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    await asyncio.sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ

async def main():
    customers = ["Alice", "Bob", "Charlie"]
    tasks = [make_coffee(customer) for customer in customers]
    await asyncio.gather(*tasks)

# สั่งให้ระบบ Async เริ่มทำงาน
if __name__ == "__main__":
    # ใช้ asyncio.run เพื่อเปิด Event Loop หลักของโปรแกรม
    asyncio.run(main())