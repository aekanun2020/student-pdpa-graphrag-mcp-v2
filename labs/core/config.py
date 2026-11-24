"""core.config — โหลดค่าตั้งจาก .env และรวมไว้ที่เดียว

ทุก Lab import ค่าจากที่นี่ เพื่อไม่ให้กระจัดกระจาย และเปลี่ยน MCP server / โมเดล
ได้จากจุดเดียว (แก้ .env อย่างเดียว)
"""
import os
from dotenv import load_dotenv

# โหลด .env จาก root ของโปรเจกต์ (หาไฟล์ขึ้นไปจากตำแหน่งนี้)
load_dotenv()

# ---- OpenRouter (LLM provider แบบ thin client) ----
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-v4.1-flash")

# ---- PDPA GraphRAG MCP server (Streamable HTTP) ----
# Default = the docker-compose server on this machine; override MCP_SERVER_URL in .env if it runs elsewhere
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8100/mcp")


def require_api_key() -> str:
    """คืน OpenRouter API key พร้อมข้อความช่วยเหลือถ้ายังไม่ได้ตั้ง"""
    if not OPENROUTER_API_KEY:
        raise SystemExit(
            "ยังไม่ได้ตั้ง OPENROUTER_API_KEY — คัดลอก .env.example เป็น .env "
            "แล้วใส่คีย์จาก https://openrouter.ai/keys"
        )
    return OPENROUTER_API_KEY
