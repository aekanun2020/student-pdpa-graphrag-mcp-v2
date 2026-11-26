#!/usr/bin/env python3
"""LAB 4 - เรียก MCP tools โดยไม่ใช้ curl และ jq (สำหรับ Windows)

ทำ 3 อย่างเดียวกับ examples/mcp_curl.sh คือ
    1. tools/list             ขอรายชื่อ tool
    2. get_penalty(sec_26)    เรียก tool ที่เดินกราฟอย่างเดียว
    3. search_pdpa            เรียก tool ที่ใช้ LLM แตกคีย์เวิร์ด แล้วพิมพ์เฉพาะ keywords

ใช้เฉพาะไลบรารีมาตรฐานของ Python ไม่ต้องติดตั้งอะไรเพิ่ม

วิธีรัน (จากโฟลเดอร์ของ repo):
    python labs/lab4/call_tools.py                                  # server ที่รันเองตาม LAB 1
    python labs/lab4/call_tools.py --url <URL ที่ผู้สอนให้>/mcp      # server ที่ผู้สอนเปิดให้
บน macOS และ Linux ใช้ python3 แทน python

ถ้าไม่ใส่ --url สคริปต์ใช้ค่าของ MCP_SERVER_URL ถ้าไม่มี ใช้ http://localhost:8100/mcp
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Windows: บังคับให้ผลลัพธ์เป็น UTF-8 เพื่อให้พิมพ์ภาษาไทยได้ทุกระบบ (แบบเดียวกับ labs/lab2/explore_graph.py)
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

DEFAULT_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8100/mcp")

p = argparse.ArgumentParser(description="LAB 4: เรียก MCP tools ด้วย Python")
p.add_argument("--url", default=DEFAULT_URL, help="ที่อยู่ของ MCP server (ค่าเริ่มต้น MCP_SERVER_URL หรือ http://localhost:8100/mcp)")
args = p.parse_args()

# header ชุดเดียวกับ examples/mcp_curl.sh: transport แบบ streamable-http บังคับให้มี Accept ที่มี application/json
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def call(request_id, method, params):
    """ส่งคำขอ JSON-RPC 1 ครั้ง แล้วคืนค่า result"""
    body = json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(args.url, data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"server ตอบ HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except OSError as e:
        sys.exit(f"ต่อ {args.url} ไม่ได้: {e}\nตรวจว่า server รันอยู่ และ URL ลงท้ายด้วย /mcp")
    # server ของ repo นี้ตอบเป็น JSON ถ้า server ตอบแบบ event-stream ให้อ่านบรรทัดที่ขึ้นต้นด้วย data:
    if text.lstrip().startswith("{"):
        reply = json.loads(text)
    else:
        data_lines = [line[5:].strip() for line in text.splitlines() if line.startswith("data:")]
        reply = json.loads(data_lines[-1])
    if "error" in reply:
        sys.exit(f"server ตอบ error: {json.dumps(reply['error'], ensure_ascii=False)}")
    return reply["result"]


def call_tool(request_id, name, arguments):
    """เรียก tool 1 ตัว แล้วแปลงข้อความที่ tool คืนมาเป็นข้อมูล"""
    result = call(request_id, "tools/call", {"name": name, "arguments": arguments})
    return json.loads(result["content"][0]["text"])


def show(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


print("== tools/list ==")
for tool in call(1, "tools/list", {})["tools"]:
    print(json.dumps(tool["name"]))

print("== get_penalty(sec_26) ==")
show(call_tool(2, "get_penalty", {"section_id": "sec_26"}))

print("== search_pdpa ==")
show(call_tool(3, "search_pdpa", {"query": "เก็บข้อมูลสุขภาพพนักงานได้ไหม", "top_k": 5})["keywords"])
