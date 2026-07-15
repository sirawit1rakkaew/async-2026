# light_utils.py
# ตัวช่วย (async) สำหรับสั่งควบคุมไฟบนเซิร์ฟเวอร์ Smart Lab Lighting System
import httpx

BASE_URL = "http://172.16.2.117:8088"


async def get_all_lights(student_id: str) -> dict:
    """ดึงสถานะไฟทั้ง 4 ดวงของนักเรียนคนหนึ่ง"""
    url = f"{BASE_URL}/api/{student_id}/lights"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return {"status": "ERROR", "detail": f"HTTP Error {response.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}


async def control_light(student_id: str, light_id: str, status: str) -> dict:
    """สั่งเปิด/ปิดไฟหนึ่งดวง (เซิร์ฟเวอร์จะหน่วงเวลาตาม hardware delay ของไฟดวงนั้น)"""
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    payload = {"status": status}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=15.0)
            if response.status_code == 200:
                return response.json()
            return {
                "status": "ERROR",
                "light_id": light_id,
                "detail": f"HTTP Error {response.status_code}: {response.text}",
            }
    except Exception as e:
        return {"status": "ERROR", "light_id": light_id, "detail": f"Connection failed: {e}"}


async def reset_lights(student_id: str) -> dict:
    """รีเซ็ตไฟทุกดวงกลับเป็น OFF"""
    url = f"{BASE_URL}/api/{student_id}/lights/reset"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return {"status": "ERROR", "detail": f"HTTP Error {response.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}
