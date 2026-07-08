import asyncio
from time import ctime

async def fetch_stock_price(server_name, delay):
    # จำลองความหน่วงของอินเทอร์เน็ต
    await asyncio.sleep(delay)
    return f"[{server_name}] Price: 150 USD"

async def main():
    # สร้าง Task 3 ตัวพร้อมกำหนด delay ตามโจทย์
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Gamma")
    }
    
    # รอจนกว่าจะมีเซิร์ฟเวอร์ตัวแรกทำงานเสร็จด้วยเงื่อนไข FIRST_COMPLETED
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    # ดึง Task ผู้ชนะออกมาแสดงผลลัพธ์
    winner_task = list(done)[0]
    
    # พิมพ์ผลลัพธ์ผู้ชนะให้ตรงกับหน้าจอโปรเจคเตอร์เป๊ะๆ
    print(f"{ctime()} Winner Result: {winner_task.result()}")
    
    # พิมพ์สรุปจำนวน Task ที่กำลังจะถูกยกเลิก โดยนับจากจำนวน pending จริง
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    
    # วนลูปสั่งยกเลิกงานที่ค้างอยู่เบื้องหลัง (แบบเงียบๆ ไม่ต้องพิมพ์แสดงบนจอ)
    for ongoing_task in pending:
        ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())