import json

# นี่คือ "สมองส่วนหลัง" ที่ง่ายที่สุดของเรา
# มีหน้าที่แค่ส่งข้อความกลับไป เพื่อพิสูจน์ว่า Python ทำงานได้บน Vercel

def handler(request):
    # สร้างข้อมูลที่จะส่งกลับไปในรูปแบบ JSON
    response_data = {
        "message": "Hello from your simplest Python Backend Function!",
        "status": "Python function is working!"
    }

    # ส่ง JSON Response กลับไป พร้อมรหัสสถานะ 200 (OK)
    return json.dumps(response_data), 200
