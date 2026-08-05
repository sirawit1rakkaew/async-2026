import asyncio
import time
import httpx

# ==========================================
# 1. Configuration & Constants
# ==========================================
STUDENT_ID = "6710301018" 
BASE_URL = "http://172.16.2.117:8088/{student_id}/monitor"

# กำหนดลำดับชิ้นส่วนและหุ่นยนต์
PARTS = ["A", "B", "C"]
ROBOTS = ["robot_1", "robot_2", "robot_3"]

# ==========================================
# 2. Async Functions Development
# ==========================================

async def reset_factory(client: httpx.AsyncClient):
    """ส่ง Request เพื่อทำการ Reset สถานะของหุ่นยนต์ทั้งหมดของรหัสนักเรียนนี้"""
    url = f"{BASE_URL}/student/{STUDENT_ID}/reset"
    try:
        async with client.post(url) as response:
            response.raise_for_status()
            print("Factory reset successful.")
    except httpx.HTTPError as e:
        print(f"Error occurred while resetting factory: {e}")

async def grab_part(client: httpx.AsyncClient, robot_id: str, part: str):
    """สั่งให้หุ่นยนต์หยิบชิ้นส่วน 1 ชิ้น"""
    url = f"{BASE_URL}/student/{STUDENT_ID}/robot/{robot_id}/grab"
    try:
        async with client.post(url, json={"part": part}) as response:
            response.raise_for_status()
            print(f"Part grabbed successfully by {robot_id}.")
    except httpx.HTTPError as e:
        print(f"Error occurred while grabbing part for {robot_id}: {e}")

async def run_robot_task(client: httpx.AsyncClient, robot_id: str):
    """สั่งให้หุ่นยนต์ 1 ตัว ทำการหยิบชิ้นส่วน A, B, และ C ตามลำดับ"""
    for part in PARTS:
        await grab_part(client, robot_id, part)

async def main():
    """ฟังก์ชันหลักสำหรับเริ่มการทำงานของหุ่นยนต์ทั้ง 4 ตัวแบบ Async"""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("Resetting Factory...")
        await reset_factory(client)
        
        start_time = time.time()
        print("Starting Async Robot Operation...")
        await asyncio.gather(
            run_robot_task(client, "robot_1"),
            run_robot_task(client, "robot_2"),
            run_robot_task(client, "robot_3")
        )
        
        elapsed_time = time.time() - start_time
        print(f"Finished all tasks in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
