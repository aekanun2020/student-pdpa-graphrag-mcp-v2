"""core.llm — OpenRouter client แบบ thin client

ใช้ OpenAI SDK ชี้ base_url ไปที่ OpenRouter — เครื่องมือแบบ low-code ที่ต่อกับ LLM
ก็เรียก API แบบเดียวกันนี้อยู่ข้างใต้
"""
from openai import OpenAI

from . import config


def build_client() -> OpenAI:
    """สร้าง OpenAI client ที่ชี้ไป OpenRouter (thin client)."""
    return OpenAI(
        api_key=config.require_api_key(),
        base_url=config.OPENROUTER_BASE_URL,
    )


def chat(messages, model: str | None = None, tools=None, **kwargs):
    """เรียก chat completion ครั้งเดียว คืน message object ของ choice แรก.

    - messages : list ของ {"role","content",...}
    - tools    : (ตัวเลือก) OpenAI-format tools สำหรับ tool calling
    """
    client = build_client()
    params = {
        "model": model or config.OPENROUTER_MODEL,
        "messages": messages,
    }
    if tools:
        params["tools"] = tools
    params.update(kwargs)
    resp = client.chat.completions.create(**params)
    return resp
