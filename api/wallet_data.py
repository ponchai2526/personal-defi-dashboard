import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# นี่คือ "กุญแจลับ Alchemy API Key" ที่เราจะใช้
# **สำคัญมาก:** คุณจะต้องตั้งค่า ALCHEMY_API_KEY ใน Environment Variables ของ Vercel ด้วย
# ห้ามใส่ API Key ตรงๆ ในโค้ดนี้เด็ดขาด!
ALCHEMY_API_KEY = os.environ.get("ALCHEMY_API_KEY")

# URL ของ Alchemy สำหรับ Polygon Mainnet
# นี่คือ "สายใยแห่งข้อมูล" ที่เชื่อมเราเข้ากับ "แกนพลังงาน Alchemy"
ALCHEMY_RPC_URL = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

# ฟังก์ชันสำหรับดึง MATIC Balance
# นี่คือส่วนที่ "สมองส่วนหลัง" คุยกับ "แกนพลังงาน Alchemy"
def get_matic_balance(wallet_address):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBalance", # Method มาตรฐานสำหรับดึง Native Token Balance
        "params": [wallet_address, "latest"] # ดึง Balance ล่าสุดของ Wallet Address ที่กำหนด
    }

    try:
        # ส่งคำขอไปยัง Alchemy
        response = requests.post(ALCHEMY_RPC_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status() # ตรวจสอบว่า HTTP request สำเร็จหรือไม่

        result = response.json()
        balance_wei = int(result["result"], 16) # Balance ที่ได้มาเป็น Wei (Hex) ต้องแปลงเป็นเลขฐาน 10
        balance_matic = balance_wei / (10**18) # 1 Ether = 10^18 Wei (MATIC ก็ใช้หน่วยนี้)
        return balance_matic
    except requests.exceptions.RequestException as e:
        print(f"Error fetching MATIC balance: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing Alchemy response: Missing key {e} or invalid format. Response: {result}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# ฟังก์ชันหลักที่ Vercel Function จะเรียกใช้
# นี่คือ "ปากประตู" ของ "สมองส่วนหลัง" ที่ "จอแสดงผลหลัก" จะคุยด้วย
def handler(request):
    # ตรวจสอบว่ามี ALCHEMY_API_KEY หรือไม่
    if not ALCHEMY_API_KEY:
        return json.dumps({"error": "ALCHEMY_API_KEY not set in environment variables."}), 500

    # Vercel functions รับ request เป็น dictionary หรือ object
    # แต่เราจะทำให้มันคล้ายกับ BaseHTTPRequestHandler.do_GET เพื่อความเข้ากันได้

    # ดึง Wallet Address จาก Query Parameters ของ URL (เช่น ?address=0x...)
    query_params = {}
    try:
        # ถ้าเป็น Vercel Function ที่ถูกเรียกจาก URL ตรงๆ
        url_parts = urlparse(request.url)
        query_params = parse_qs(url_parts.query)
    except AttributeError:
        # ถ้า request มาจาก Vercel's internal testing (เป็น dict/object)
        if 'query' in request and request['query']:
            query_params = request['query']

    wallet_address = query_params.get("address", [None])[0] # Get the first value if it's a list


    if not wallet_address:
        return json.dumps({"error": "Wallet address is required."}), 400

    # ดึง MATIC Balance
    matic_balance = get_matic_balance(wallet_address)

    if matic_balance is not None:
        # ส่งข้อมูลกลับไปให้ Frontend
        response_data = {
            "tokens": [
                {
                    "symbol": "MATIC",
                    "name": "Polygon",
                    "balance": f"{matic_balance:.5f}", # Format ให้เป็นทศนิยม 5 ตำแหน่ง
                    "price": 0, # ยังไม่มีราคาจริงในตอนนี้
                    "value": 0,  # ยังไม่มีมูลค่าจริงในตอนนี้
                    "change24h": 0, # ยังไม่มีการเปลี่ยนแปลง 24h
                    "icon": "https://cryptologos.cc/logos/polygon-matic-logo.png"
                }
            ]
        }
        return json.dumps(response_data), 200 # ส่ง JSON กลับไปพร้อม Status 200 OK
    else:
        return json.dumps({"error": "Failed to fetch MATIC balance."}), 500

# นี่คือสิ่งที่ Vercel จะเรียกใช้เมื่อมี HTTP request เข้ามา
# ถ้า deploy เป็น Vercel Function ปกติ Vercel จะหา handler function
# สำหรับการทดสอบใน GitHub Editor มันจะมองข้ามส่วนนี้
def do_GET(self):
    # This part is mostly for local testing with BaseHTTPRequestHandler
    # Vercel's environment provides the 'request' object directly to the 'handler' function
    pass
