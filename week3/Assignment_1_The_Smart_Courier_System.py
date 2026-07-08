import asyncio


async def delivery_task(package_id: str, duration: float) -> str:
    """คอรูทีนจำลองการส่งพัสดุ 1 ชิ้น โดยใช้เวลาตาม duration ที่กำหนด"""
    print(f"Courier started delivering {package_id}...")
    try:
        await asyncio.sleep(duration)
    except asyncio.CancelledError:
        # ดักจับตอนถูกยกเลิกระหว่างทาง
        print("Delivery Canceled! Returning package to warehouse.")
        raise  # ต้อง re-raise เสมอ เพื่อให้ asyncio รู้ว่า Task นี้ถูกยกเลิกจริง ๆ
    else:
        result = f"Package {package_id} Delivered!"
        print(f"[DONE] {result}")
        return result


async def main():
    # package_id = str(input("กรุณาใส่รหัสพัสดุ: "))
    # duration = float(input("กรุณาใส่เวลาที่ใช้ในการส่งพัสดุ (วินาที): "))
    # 2) สร้าง Task จาก delivery_task และตั้งชื่อ Task ว่า "Express-Courier"
    task = asyncio.create_task(
        delivery_task(package_id="P001", duration=2.0),
        name="Express-Courier",
    )

    # 3) จำลองว่าระหว่างพัสดุกำลังเดินทาง ผ่านไป 2 วินาที แล้วมาเช็กสถานะ
    await asyncio.sleep(2)
    print(f"Checking task {task.get_name()}. Is it done? {task.done()}")

    # 4) ถ้าผ่านไป 2 วินาทีแล้วยังไม่เสร็จ ให้ยกเลิกงานทันที
    if not task.done():
        print(f"Taking too long! Canceling the task...")
        task.cancel()

    # รอให้ Task จบจริง ๆ (ไม่ว่าจะเสร็จหรือถูกยกเลิก) และดักจับ CancelledError ฝั่ง caller ด้วย
    try:
        result = await task
        print(f"[RESULT] {result}")
    except asyncio.CancelledError:
        #print("Delivery Canceled! Returning package to warehouse.")
        pass
    # 5) ตรวจสอบสถานะภายนอกว่า Task ถูกยกเลิกจริงหรือไม่ด้วย .cancelled()
    print(f"Final verify: Is task officially canceled? {task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
