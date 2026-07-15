# light_client.py
# สั่งเปิดไฟทั้ง 4 ดวงพร้อมกันแบบ async (concurrent) ด้วย asyncio.gather
# เทียบให้เห็นชัดว่าเร็วกว่าการสั่งทีละดวงแบบ sequential
import asyncio
from time import ctime, perf_counter

from light_utils import get_all_lights, control_light, reset_lights

MY_STUDENT_ID = "6710301018"
ALL_LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


def show_status(title: str, lights: dict) -> None:
    print(f"\n{ctime()} | {title}")
    for light_id in ALL_LIGHTS:
        info = lights.get(light_id, {})
        print(
            f"   - {light_id}: {info.get('status', '?'):<3} "
            f"| delay {info.get('delay', '?')}s | {info.get('name', '')}"
        )


async def main():
    print(f"{ctime()} | === สั่งควบคุมไฟของนักเรียน {MY_STUDENT_ID} ===")

    # 0) เริ่มจากรีเซ็ตให้ทุกดวง OFF ก่อน แล้วดูสถานะเริ่มต้น
    await reset_lights(MY_STUDENT_ID)
    show_status("สถานะเริ่มต้น (ก่อนสั่ง)", await get_all_lights(MY_STUDENT_ID))

    # 1) เปิดไฟทั้ง 4 ดวง "พร้อมกัน" ด้วย gather
    #    ถ้าสั่งทีละดวงจะใช้เวลา 0.5+1.2+2.0+0.8 = 4.5 วินาที
    #    แต่ทำพร้อมกันจะใช้เวลาเท่าดวงที่ช้าสุด = 2.0 วินาที
    print(f"\n{ctime()} | 🔆 เปิดไฟทั้ง 4 ดวงพร้อมกัน...")
    start = perf_counter()

    tasks = [control_light(MY_STUDENT_ID, lid, "ON") for lid in ALL_LIGHTS]
    results = await asyncio.gather(*tasks)

    elapsed = perf_counter() - start
    for r in results:
        print(f"{ctime()} | ✅ {r.get('light_id')} -> {r.get('current_status', r.get('detail'))}")
    print(f"{ctime()} | ⏱️  ใช้เวลารวม {elapsed:.2f} วินาที (เท่าดวงที่ช้าสุด ~2.0s)")

    # 2) ตรวจสอบสถานะหลังเปิด
    show_status("สถานะหลังเปิดไฟทั้งหมด", await get_all_lights(MY_STUDENT_ID))

    # 3) รีเซ็ตปิดไฟทุกดวง
    print(f"\n{ctime()} | 🔄 รีเซ็ตไฟทุกดวง...")
    msg = await reset_lights(MY_STUDENT_ID)
    print(f"{ctime()} | {msg.get('message', msg)}")
    show_status("สถานะหลังรีเซ็ต", await get_all_lights(MY_STUDENT_ID))


if __name__ == "__main__":
    asyncio.run(main())
