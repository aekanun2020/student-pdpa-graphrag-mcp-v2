# LAB 3 ทำตามสไลด์ทีละขั้น พร้อมผลที่ได้

เอกสารนี้แสดงผลของการทำ LAB 3 ตามสไลด์ M1 หน้า "Hands-on LAB 3: สร้าง Knowledge Graph" ทุกขั้น ใช้เทียบกับผลบนเครื่องของคุณได้

- **ทำเมื่อ:** 25 พ.ย. 2569 บน macOS 27.0.1 ด้วย Python 3.9.6 จาก commit [`d74bf9c`](https://github.com/aekanun2020/student-pdpa-graphrag-mcp-v2/commit/d74bf9c) ของ repo นี้
- **ยังไม่ได้ทดสอบบน Windows**
- **ภาพในเอกสารนี้สร้างจากข้อความที่ terminal พิมพ์ออกมาจริง ไม่ใช่ภาพถ่ายหน้าจอ**
- **Python ที่ใช้:** รันใน virtual environment ใหม่ที่ยังไม่มี `networkx`

LAB นี้ไม่ต้องเปิด server สคริปต์สร้างกราฟลงโฟลเดอร์ `build/` แล้วให้ตรวจและเทียบกับกราฟที่ใช้จริงใน `data/`

## 1. เตรียมโฟลเดอร์ของ repo

สไลด์ให้รันจากโฟลเดอร์ของ repo เดียวกับ LAB 2 ถ้ามีอยู่แล้ว ข้ามข้อนี้

```sh
git clone https://github.com/aekanun2020/student-pdpa-graphrag-mcp-v2.git
cd student-pdpa-graphrag-mcp-v2
```

![ผลของคำสั่ง git clone](lab3-walkthrough/01-clone-001.png)

## 2. สร้างกราฟ

```sh
python3 scripts/build_graph.py
```

ผลยาว จึงแบ่งเป็น 3 ภาพเรียงตามลำดับ ทุกบรรทัดอยู่ครบ

![ผลของคำสั่งสร้างกราฟ ส่วนที่ 1](lab3-walkthrough/03-build-001.png)

![ผลของคำสั่งสร้างกราฟ ส่วนที่ 2](lab3-walkthrough/03-build-002.png)

![ผลของคำสั่งสร้างกราฟ ส่วนที่ 3](lab3-walkthrough/03-build-003.png)

บรรทัด `Output:` แสดง path ของโฟลเดอร์ `build/` บนเครื่องที่รัน บนเครื่องของคุณ path ส่วนหน้าจะต่างจากในภาพ

### ดูไฟล์ที่สร้างขึ้น

คำสั่งนี้เป็นคำสั่งตรวจเพิ่ม ไม่ได้อยู่ในสไลด์

```sh
ls -1 build
```

![รายชื่อไฟล์ในโฟลเดอร์ build](lab3-walkthrough/04-build-files-001.png)

## 3. ติดตั้ง networkx และตรวจกราฟที่สร้าง

```sh
python3 -m pip install networkx
```

![ผลของคำสั่งติดตั้ง networkx](lab3-walkthrough/06-install-networkx-001.png)

```sh
python3 scripts/validate_graph.py build/pdpa_knowledge_graph.json
```

![ผลของคำสั่งตรวจกราฟ](lab3-walkthrough/07-validate-001.png)

## 4. เทียบกับกราฟที่ใช้จริง

```sh
cmp build/pdpa_knowledge_graph.json data/pdpa_knowledge_graph.json
```

![ผลของคำสั่ง cmp](lab3-walkthrough/08-compare-001.png)

คำสั่ง `cmp` ไม่พิมพ์อะไร ภาพจึงมีเฉพาะบรรทัดคำสั่ง แปลว่าไฟล์ทั้งสองตรงกันทุกไบต์

## 5. เทียบกับผลที่สไลด์ระบุ

| รายการ | สไลด์บอกว่า | ได้จริง | ดูได้ที่ |
|---|---|---|---|
| จำนวนไฟล์ที่เขียน | 5 ไฟล์ | 5 ไฟล์ | ข้อ 2 รายชื่อไฟล์ |
| โฟลเดอร์ปลายทาง | `build/` | `build/` | ข้อ 2 บรรทัด `Output:` |
| ไฟล์ใน `data/` | ไม่ถูกทับ | SHA-256 ของ `data/pdpa_knowledge_graph.json` ก่อนและหลังรันเท่ากัน | ไม่มีภาพ |
| Total Nodes | 190 | 190 | ข้อ 2 ภาพส่วนที่ 1 |
| Total Edges | 382 | 382 | ข้อ 2 ภาพส่วนที่ 1 |
| ผลตรวจ | ทุกบรรทัดขึ้น `[OK]` | 5 จาก 5 บรรทัดขึ้น `[OK]` | ข้อ 3 |
| เทียบด้วย `cmp` | ไม่พิมพ์อะไร | ไม่พิมพ์อะไร | ข้อ 4 |

ผลตรงกับสไลด์ทุกรายการ
