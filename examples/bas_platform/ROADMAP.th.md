# Roadmap สั้นสำหรับ BAS Platform Wrapper

## สัปดาห์ 2: Caldera API Wrapper
- ใช้ `backend/caldera_client.py` เป็นจุดรวมการเรียก API
- เริ่มจาก flow สำคัญ: trigger operation, list operation, query state
- ทำ unit tests แยกจาก integration tests (mock Caldera)

## สัปดาห์ 3: SIEM Connector (Wazuh)
- ใช้ `backend/collectors/wazuh.py` เป็นตัวอย่าง connector แรก
- normalize schema ให้เป็น model กลางก่อนส่งเข้า correlation
- เพิ่ม retry/backoff และ token cache เพื่อความเสถียร

## สัปดาห์ 4: Correlation + Scheduler
- วาง logic ใน `backend/correlation/engine.py`
- เก็บผล correlation ลง DB แล้วส่งต่อ frontend
- ใช้ APScheduler รันทุก 3-5 นาที (หรือ event-driven ถ้าต้องการ near real-time)

## สัปดาห์ 5+: Container + Frontend Integration
- ใช้ `docker-compose.wrapper.yml` เป็นจุดเริ่ม
- แยก env ของ dev/stage/prod
- ต่อ frontend ให้เรียก wrapper API แทนยิง Caldera ตรง

## ข้อแนะนำ architecture
- ให้ wrapper เป็น owner ของ business logic ทั้งหมด
- Caldera ทำหน้าที่ execution engine
- SIEM/EDR connectors แยกเป็น module/adapter เพื่อ scale ไปหลายผู้ให้บริการได้ง่าย
