import asyncio
import httpx

BASE_URL = "http://172.16.2.117:8088"


async def fetch_stock_price(server_name: str) -> str:
    """
    Coroutine ดึงราคาหุ้นจาก Stock Price API Server จริงของอาจารย์
    ห้ามรับ delay เอง เพราะความหน่วงเกิดขึ้นจริงที่ฝั่ง Server แล้ว
    """
    url = f"{BASE_URL}/price/{server_name}"
    async with httpx.AsyncClient() as client:
        print(f"[REQUEST] กำลังยิง request ไปที่ {server_name} -> {url}")
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        price = data["price"]
        return f"[{server_name}] Price: {price} USD"


async def main():
    servers = ["Alpha", "Beta", "Gamma"]

    # แตกเป็น asyncio.Task ทั้ง 3 ตัว ส่งเข้าคิวรันพร้อมกันใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price(name), name=name)
        for name in servers
    }

    # ดีดตัวหลุดจากการรอทันทีเมื่อมีเซิร์ฟเวอร์ตัวแรกตอบกลับสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน
    for winner in done:
        try:
            result = winner.result()
            print(f"[WINNER] ผลลัพธ์ที่เร็วที่สุด: {result}  (Task: {winner.get_name()})")
        except Exception as exc:
            # กรณี server ตอบ error/timeout ก็ยังนับว่า "เสร็จ" (done) แต่ result() จะ raise exception
            print(f"[ERROR] Task {winner.get_name()} ล้มเหลว: {exc!r}")

    # ==== Anti-Memory Leak: วนลูปยกเลิก Task ที่ยังค้างอยู่ใน pending ให้หมดสิ้น ====
    print(f"[CLEANUP] พบ Task ที่ยังทำงานค้างอยู่ {len(pending)} ตัว -> สั่งยกเลิกทั้งหมด")
    for task in pending:
        print(f"  -> ยกเลิก Task: {task.get_name()} (ตัด HTTP request ที่ยังวิ่งค้างอยู่)")
        task.cancel()

    # รอให้ทุก Task ที่ถูกยกเลิกจัดการ cleanup จนจบจริง ๆ (httpx จะปิด connection ให้เอง)
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)

    for task in pending:
        print(f"[CLEANUP] {task.get_name()}.cancelled() = {task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
