#!/usr/bin/env python3
"""LAB 2 - อ่านและวิเคราะห์ data/pdpa_knowledge_graph.json

ขั้นที่ 1-5 ใช้เฉพาะไลบรารีมาตรฐานของ Python ไม่ต้องติดตั้งอะไรเพิ่ม
ขั้นที่ 6 ใช้ networkx ถ้าเครื่องไม่มี สคริปต์จะข้ามขั้นนี้และบอกวิธีติดตั้ง

วิธีรัน (จากโฟลเดอร์ของ repo):
    python3 labs/lab2/explore_graph.py                 # เริ่มเดินจากมาตรา 41
    python3 labs/lab2/explore_graph.py --section 26    # เริ่มเดินจากมาตราอื่น
    python3 labs/lab2/explore_graph.py --step 3        # ดูเฉพาะขั้นที่ 3
บน Windows ใช้ python แทน python3

สคริปต์นี้อ่านไฟล์อย่างเดียว ไม่แก้ไฟล์กราฟ และไม่ต้องเปิด server
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

# Windows: เมื่อผลลัพธ์ไม่ได้ออกที่หน้าต่าง console โดยตรง (Git Bash, > ไฟล์) Python ใช้ code page ของเครื่อง
# ซึ่งอาจเขียนภาษาไทยไม่ได้ จึงบังคับให้ผลลัพธ์เป็น UTF-8 ทุกระบบ
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(HERE, "..", "..", "data", "pdpa_knowledge_graph.json")

p = argparse.ArgumentParser(description="LAB 2: อ่านและวิเคราะห์ไฟล์กราฟ PDPA")
p.add_argument("path", nargs="?", default=DEFAULT_PATH, help="ไฟล์กราฟ (ค่าเริ่มต้น data/pdpa_knowledge_graph.json)")
p.add_argument("--section", type=int, default=41, help="เลขมาตราที่ใช้เริ่มเดินในขั้นที่ 5 (ค่าเริ่มต้น 41)")
p.add_argument("--step", type=int, choices=range(1, 7), help="แสดงเฉพาะขั้นที่ระบุ (1-6)")
args = p.parse_args()

with open(args.path, encoding="utf-8") as f:
    graph = json.load(f)
nodes, edges, meta = graph["nodes"], graph["edges"], graph.get("metadata", {})
by_id = {n["id"]: n for n in nodes}


def show(step):
    return args.step is None or args.step == step


def head(step, title):
    print(f"\n=== ขั้นที่ {step}: {title} ===")


def short(value, limit=60):
    text = str(value).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "..."


# ---------------------------------------------------------------- ขั้นที่ 1
if show(1):
    head(1, "กราฟมีกี่โหนด กี่เส้น")
    print(f"นับจากข้อมูล  : {len(nodes)} โหนด / {len(edges)} เส้น")
    print(f"metadata บอกว่า : {meta.get('node_count')} โหนด / {meta.get('edge_count')} เส้น")

# ---------------------------------------------------------------- ขั้นที่ 2
if show(2):
    head(2, "Node Type มีอะไรบ้าง และแต่ละชนิดมี property อะไร")
    count = Counter(n["label"] for n in nodes)
    props = defaultdict(set)
    for n in nodes:
        props[n["label"]].update(k for k in n if k not in ("id", "label"))
    print(f"{'Node Type':<13}{'จำนวน':>6}  properties")
    for label in sorted(count, key=lambda x: (-count[x], x)):
        print(f"{label:<13}{count[label]:>6}  {', '.join(sorted(props[label]))}")
    print(f"รวม {len(count)} ชนิด / {sum(count.values())} โหนด")

# ---------------------------------------------------------------- ขั้นที่ 3
if show(3):
    head(3, "Relationship Type มีอะไรบ้าง และเชื่อม Node Type ใดกับใด")
    pairs = defaultdict(Counter)
    with_order = Counter()
    for e in edges:
        src, tgt = by_id[e["source"]]["label"], by_id[e["target"]]["label"]
        pairs[e["relationship"]][(src, tgt)] += 1
        with_order[e["relationship"]] += "order" in e
    print(f"{'Relationship Type':<26}{'จำนวน':>6}  ต้นทาง -> ปลายทาง")
    for rel in sorted(pairs, key=lambda x: (-sum(pairs[x].values()), x)):
        for (src, tgt), n in pairs[rel].most_common():
            print(f"{rel:<26}{n:>6}  {src} -> {tgt}")
    print(f"รวม {len(pairs)} ประเภท / {len(edges)} เส้น")
    print(f"เส้นที่มี property 'order': {sum(with_order.values())} เส้น "
          f"({', '.join(sorted(r for r, n in with_order.items() if n))})")

# ---------------------------------------------------------------- ขั้นที่ 4
if show(4):
    head(4, "โหนด 1 ตัว และเส้น 1 เส้น ทั้งแถว (instance)")
    law = by_id["PDPA_2562"]
    print("โหนด PDPA_2562:")
    for k, v in law.items():
        print(f"    {k:<16}= {short(v)}")
    edge = next(e for e in edges if e["source"] == "PDPA_2562" and e["target"] == "ch3")
    print("เส้นจาก PDPA_2562 ไป ch3:")
    for k, v in edge.items():
        print(f"    {k:<16}= {v}")

# ---------------------------------------------------------------- ขั้นที่ 5
if show(5):
    start = f"sec_{args.section}"
    head(5, f"เดินจากมาตรา {args.section} ไปยังโหนดรอบข้าง")
    if start not in by_id:
        print(f"ไม่พบโหนด {start} ในกราฟ (มาตรามีเลข 1-96)")
    else:
        out_edges = [e for e in edges if e["source"] == start]
        in_edges = [e for e in edges if e["target"] == start]
        print(f"เส้นที่ออกจาก {start}: {len(out_edges)} เส้น")
        for e in out_edges:
            print(f"    {start} -[{e['relationship']}]-> {e['target']} ({by_id[e['target']]['label']})")
        print(f"เส้นที่ชี้เข้า {start}: {len(in_edges)} เส้น")
        for e in in_edges:
            print(f"    {e['source']} ({by_id[e['source']]['label']}) -[{e['relationship']}]-> {start}")

        # หาโทษภายใน 2 hop โดยเดินได้ทั้งตามทิศและย้อนทิศของเส้น แบบเดียวกับ tool get_penalty
        neighbours = defaultdict(list)
        for e in edges:
            neighbours[e["source"]].append((e["target"], f"-[{e['relationship']}]->"))
            neighbours[e["target"]].append((e["source"], f"<-[{e['relationship']}]-"))
        found = []
        for mid, step1 in neighbours[start]:
            if by_id[mid]["label"] == "Penalty":
                found.append(f"{start} {step1} {mid}")
            for end, step2 in neighbours[mid]:
                if by_id[end]["label"] == "Penalty" and end != start:
                    found.append(f"{start} {step1} {mid} {step2} {end}")
        print(f"เส้นทางจาก {start} ถึงโหนดชนิด Penalty ภายใน 2 hop: {len(found)} เส้นทาง")
        for path in found:
            print(f"    {path}")
            pen = by_id[path.split()[-1]]
            print(f"        โทษ: {short(pen.get('description', ''), 90)}")

# ---------------------------------------------------------------- ขั้นที่ 6
if show(6):
    head(6, "โหลดเข้า NetworkX แบบเดียวกับที่ server โหลดเส้น")
    try:
        import networkx as nx
    except ImportError:
        print("เครื่องนี้ยังไม่มี networkx จึงข้ามขั้นนี้ ติดตั้งได้ด้วย: pip install networkx")
    else:
        G = nx.DiGraph()
        for n in nodes:
            G.add_node(n["id"], **{k: v for k, v in n.items() if k != "id"})
        for e in edges:
            G.add_edge(e["source"], e["target"], **{k: v for k, v in e.items() if k not in ("source", "target")})
        print(f"NetworkX: {G.number_of_nodes()} โหนด / {G.number_of_edges()} เส้น")
        print(f"attribute ของเส้น PDPA_2562 -> ch3 : {G.edges['PDPA_2562', 'ch3']}")
        print("สังเกต: source และ target ไม่อยู่ใน attribute แล้ว เพราะ NetworkX ใช้ 2 ค่านี้เป็นตัวเส้นเอง")
        print("        ในไฟล์ JSON เป็น property ของเส้น แต่ในกราฟที่โหลดแล้วเป็นปลาย 2 ข้างของเส้น")
