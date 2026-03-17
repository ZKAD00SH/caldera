# BAS Wrapper Starter (บน Caldera)

โฟลเดอร์นี้เป็น starter kit สำหรับแนวทางที่คุณวางไว้: สร้างแพลตฟอร์มของตัวเองแล้ว orchestrate MITRE Caldera ผ่าน REST API

## โครงสร้าง

```text
examples/bas_platform/
├── backend/
│   ├── main.py
│   ├── caldera_client.py
│   ├── scheduler.py
│   ├── models.py
│   ├── collectors/
│   │   └── wazuh.py
│   └── correlation/
│       └── engine.py
├── requirements.txt
└── docker-compose.wrapper.yml
```

## การใช้งานเร็ว

1. รัน Caldera แยกตามปกติ (เช่น `http://localhost:8888`)  
2. ติดตั้ง dependency

```bash
cd examples/bas_platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. ตั้งค่า environment

```bash
export CALDERA_URL="http://localhost:8888"
export CALDERA_API_KEY="redacted"
export WAZUH_URL="http://localhost:55000"
export WAZUH_USERNAME="wazuh-wui"
export WAZUH_PASSWORD="redacted"
```

4. รัน wrapper API

```bash
uvicorn backend.main:app --reload --port 9000
```

## Endpoint สำคัญ

- `GET /health` ตรวจสุขภาพ service
- `POST /operations/trigger` trigger operation บน Caldera
- `POST /correlation/run-once` ดึง alert จาก Wazuh แล้ว match กับ operation ล่าสุด

> โค้ดนี้เป็น starter สำหรับสัปดาห์ 2-4 (API wrapper + collector + correlation + scheduler) และตั้งใจให้ปรับต่อเข้ากับ frontend/DB ของคุณ
