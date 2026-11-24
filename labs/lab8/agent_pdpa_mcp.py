"""
Lab 8 — สร้าง Agent ที่เชื่อมต่อกับ PDPA GraphRAG MCP Server ของ repo นี้

agent loop แบบ "while loop + model + tools" ที่ใช้ **MCP tools จริง**:
  - MCP Tool Discovery อัตโนมัติผ่าน Streamable HTTP (core.mcp_client)
  - แปลง MCP inputSchema -> OpenAI function (core.registry.mcp_to_openai_tools)
  - Tool Registry รวม tools จากหลาย MCP server (ที่นี่ต่อ PDPA GraphRAG เป็นแกน)

server ฝั่ง PDPA GraphRAG เปิดเป็น MCP Server ไว้แล้ว (docker compose ของ repo นี้)
— Lab นี้เขียน MCP client เป็น Python เองแล้วต่อเข้ากับ agent loop แทนการใช้ client สำเร็จรูป เช่น Claude Desktop หรือ LangFlow

รัน:  python labs/lab8/agent_pdpa_mcp.py "เก็บข้อมูลสุขภาพพนักงานได้ไหม มีโทษอะไร"
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from labs.core import llm, config
from labs.core.registry import ToolRegistry

SYSTEM = (
    "คุณคือที่ปรึกษากฎหมาย PDPA ที่ตอบคำถามโดยค้นจาก GraphRAG ผ่าน MCP tools เท่านั้น ห้ามเดาตัวบทจากความจำ "
    "ขั้นตอน: เรียก search_pdpa ก่อนเสมอเพื่อได้ context + มาตราที่เกี่ยวข้อง แล้วใช้ get_related_sections('sec_<เลข>') หามาตราเชื่อมโยง "
    "ถ้าถามเรื่องโทษให้เรียก get_penalty('sec_<เลข>') ก่อนอ้างอิงตัวบทให้เรียก get_section_text('sec_<เลข>') อ่านตัวบทจริง "
    "ตอบเป็นภาษาไทย อ้างเลขมาตราชัดเจน แยก 'บทบัญญัติ' ออกจาก 'คำแนะนำ'"
)


def run_agent(question: str, registry: ToolRegistry, max_steps: int = 8):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for step in range(1, max_steps + 1):
        resp = llm.chat(messages=messages, tools=registry.openai_tools, temperature=0)
        msg = resp.choices[0].message

        if msg.tool_calls:
            print(f"[step {step}] THINK -> ขอเรียก {len(msg.tool_calls)} tool")
            messages.append({
                "role": "assistant", "content": msg.content or "",
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
            })
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments or "{}")
                preview = json.dumps(args, ensure_ascii=False)
                if len(preview) > 80:
                    preview = preview[:80] + "..."
                print(f"           TOOL_USE {call.function.name}({preview})")
                result = registry.dispatch(call.function.name, args)
                messages.append({
                    "role": "tool", "tool_call_id": call.id,
                    "content": result,   # OBSERVE: ป้อนผล tool กลับเข้า context
                })
            continue

        print(f"[step {step}] END_TURN")
        print("-" * 60)
        print(f"[answer]\n{msg.content}")
        return msg.content

    print("[!] ถึงขีดจำกัดจำนวนรอบแล้ว")
    return None


def main():
    # ---- Tool Registry : รองรับหลาย MCP server (ที่นี่ต่อ PDPA GraphRAG MCP server เป็นแกน) ----
    registry = ToolRegistry()
    n = registry.add_server(config.MCP_SERVER_URL)
    # ตัวอย่างต่อ MCP server เพิ่มอีกตัว: registry.add_server("http://localhost:8000/mcp")
    print(f"[MCP] เชื่อม {config.MCP_SERVER_URL}")
    print(f"[MCP] ค้นพบ {n} tools: {registry.tool_names}\n")

    q = sys.argv[1] if len(sys.argv) > 1 else "เก็บข้อมูลสุขภาพพนักงานได้ไหม ถ้าฝ่าฝืนมีโทษอะไร"
    print(f"[user] {q}")
    try:
        run_agent(q, registry)
    finally:
        registry.close()


if __name__ == "__main__":
    main()
