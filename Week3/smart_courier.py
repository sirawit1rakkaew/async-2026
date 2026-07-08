import asyncio
from time import ctime

async def delivery_task(package_id, duration):
    try:
        # ปรับข้อความให้ตรงกับบรรทัดแรกของอาจารย์
        print(f"{ctime()} Courier started delivering {package_id}...")
        
        await asyncio.sleep(duration)
        return f"Package {package_id} Delivered!"
        
    except asyncio.CancelledError:
        # ปรับข้อความให้ตรงกับบรรทัดที่ 4 ของอาจารย์
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise 

async def main():
    # สร้าง Task และตั้งชื่อ
    task = asyncio.create_task(delivery_task(package_id="P001", duration=5.0))
    task.set_name("Express-Courier")
    
    # จำลองเวลารอ 2 วินาที
    await asyncio.sleep(2.0)
    
    # ดึงค่าสถานะและชื่อเพื่อมาปริ้น
    is_done = task.done()
    task_name = task.get_name()
    
    # ปรับข้อความให้ตรงกับบรรทัดที่ 2 ของอาจารย์
    print(f"{ctime()} Checking task '{task_name}'. Is it done? {is_done}")
    
    if not is_done:
        # ปรับข้อความให้ตรงกับบรรทัดที่ 3 ของอาจารย์
        print(f"{ctime()} Taking too long! Canceling the task...")
        task.cancel()
        
    try:
        await task
    except asyncio.CancelledError:
        pass 
        
    # ปรับข้อความให้ตรงกับบรรทัดที่ 5 ของอาจารย์
    is_cancelled = task.cancelled()
    print(f"{ctime()} Final verify: Is task officially canceled? {is_cancelled}")

if __name__ == "__main__":
    asyncio.run(main())