import asyncio


async def fetch_stock_price(server_name: str, delay: float) -> str:
    """จำลองการดึงราคาหุ้นจากเซิร์ฟเวอร์แต่ละสาขา ซึ่งแต่ละสาขาตอบสนองช้า-เร็วไม่เท่ากัน"""
    #print(f"[REQUEST] กำลังดึงราคาจากเซิร์ฟเวอร์ {server_name} (คาดว่าใช้เวลา {delay} วินาที)")
    await asyncio.sleep(delay)
    return f"[{server_name}] Price: 150 USD"


async def main():
    # แตก Task ขึ้นมา 3 ตัวพร้อมกันใน Event Loop
    task_alpha = asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Alpha")
    task_beta = asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Beta")
    task_gamma = asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Gamma")

    tasks = {task_alpha, task_beta, task_gamma}

    # เลือกใช้ asyncio.wait() เพราะรองรับ return_when=FIRST_COMPLETED
    # (asyncio.gather() ไม่มีพารามิเตอร์นี้ ต้องรอครบทุกตัวเสมอ จึงไม่เหมาะกับโจทย์นี้)
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะ (เสร็จก่อนเพื่อน)
    for winner in done:
        result = winner.result()
        print(f"Winner Result: {result}  ")#(Task: {winner.get_name()})

    # ==== วนลูปเคลียร์ระบบ: ยกเลิก Task ที่ยังค้างอยู่ (pending) ทั้งหมด ====
    print(f"Cleaning up {len(pending)} pending tasks...")
    for task in pending:
        # print(f"  -> ยกเลิก Task: {task.get_name()}")
        task.cancel()

    # รอให้ Task ที่ถูกยกเลิกทำ cleanup จบจริง ๆ กัน warning
    # "Task exception was never retrieved" และป้องกัน memory leak หลังบ้าน
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)

    # for task in pending:
    #     print(f"[CLEANUP] {task.get_name()}.cancelled() = {task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
