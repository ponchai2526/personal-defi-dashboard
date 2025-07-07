import os
import json

# นี่คือ "สมองส่วนหลัง" ตัวจิ๋วของเรา
# มีหน้าที่แค่ตรวจสอบว่า ALCHEMY_API_KEY ถูกตั้งค่าใน Vercel Environment Variables หรือไม่

def handler(request):
    # ดึงค่า ALCHEMY_API_KEY จาก Environment Variables
    # os.environ.get จะช่วยให้เราอ่านค่าจากตัวแปรที่ตั้งค่าไว้ใน Vercel
    alchemy_api_key_value = os.environ.get("ALCHEMY_API_KEY")

    if alchemy_api_key_value:
        # ถ้ามีค่า API Key แสดงว่าตั้งค่าถูกต้อง
        response_message = f"Alchemy API Key ถูกตั้งค่าแล้ว: {alchemy_api_key_value}"
        status_code = 200 # รหัส 200 หมายถึงสำเร็จ
    else:
        # ถ้าไม่มีค่า API Key แสดงว่ายังไม่ได้ตั้งค่า หรือตั้งค่าผิด
        response_message = "ERROR: Alchemy API Key ยังไม่ได้ถูกตั้งค่าใน Vercel Environment Variables!"
        status_code = 500 # รหัส 500 หมายถึงเกิดข้อผิดพลาดที่ Server

    # ส่งข้อความกลับไปในรูปแบบ JSON
    return json.dumps({"status": response_message}), status_code
