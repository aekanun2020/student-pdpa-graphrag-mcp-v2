"""
core — โมดูลกลางฝั่ง agent ที่ labs/lab8 ใช้

  - config.py  : โหลด .env และค่าตั้งต้น
  - llm.py     : OpenRouter client (thin client)
  - mcp_client.py : MCP client ผ่าน Streamable HTTP
  - registry.py   : Tool Registry รวม tools จาก MCP server

ปรัชญา: "Minimal Agent = while loop + model + tools" — เขียนเองด้วย Pure Python ไม่ใช้ framework
"""
