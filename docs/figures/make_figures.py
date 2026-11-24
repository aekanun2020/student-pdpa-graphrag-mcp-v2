"""Draw docs/fig1_architecture.png and docs/fig3_search_pipeline.png.

Source of the two README figures. Every number and name below was checked against the code and data
at the commit that last changed this file; if retrieval.py, the graph or the tools change, edit the
text here and re-run:

    python docs/figures/make_figures.py

Needs matplotlib only. Output goes to docs/.

The PNGs in the repo were drawn with matplotlib 3.11.2 on macOS. Other versions set text slightly wider or
narrower (3.9.2: about 1.5% wider), so re-running with another version changes every line of both figures.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent
# Thai text needs a font whose vowel and tone marks stack correctly without a shaping engine. On macOS
# "Arial Unicode MS" does in matplotlib; Thonburi, Tahoma, Sarabun and Noto Sans Thai do not.
plt.rcParams["font.family"] = ["Arial", "Arial Unicode MS", "DejaVu Sans"]

INK, GREY, LINE = "#1a1a1a", "#555555", "#c9cabd"
PANEL, BLUE_FILL, BLUE_EDGE = "#ececea", "#dde6f0", "#2f7de1"


def canvas(w, h, title):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    ax.text(64, 52, title, fontsize=14.5, fontweight="bold", color=INK, va="center")
    return fig, ax


def box(ax, x, y, w, h, title, lines, fill="white", edge=LINE, lw=1.4, center=False, title_size=12.5, mono=()):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12",
                                fc=fill, ec=edge, lw=lw, zorder=2))
    tx, ha = (x + w / 2, "center") if center else (x + 22, "left")
    t_thai = _has_thai(title)   # same rule as the body lines below
    ax.text(tx, y + 34 + (_drop(ax, title_size, None, "bold") if t_thai else 0), title, fontsize=title_size,
            fontweight="bold", color=INK, ha=ha, va="baseline" if t_thai else "center", zorder=3)
    for i, line in enumerate(lines):
        text, colour = (line, INK) if isinstance(line, str) else line
        family = "DejaVu Sans Mono" if i in mono else None
        size = 9.6 if i in mono else 10.6
        # va="center" centres the ink of the line, so a Thai line with tall vowel or tone marks sits lower
        # than its neighbours. Lines with Thai are placed by baseline instead, at the baseline a Latin-only
        # line gets from "center"; Latin-only lines keep "center" so their pixels do not change.
        thai = _has_thai(text)
        ax.text(tx, y + 63 + 28.5 * i + (_drop(ax, size, family) if thai else 0), text, fontsize=size,
                color=colour, ha=ha, va="baseline" if thai else "center", zorder=3, family=family)


def _has_thai(text):
    return any("\u0e00" <= ch <= "\u0e7f" for ch in text)


def _drop(ax, size, family, weight=None):
    """Distance in data units from the centre of a Latin line ("lp") down to its baseline."""
    fig = ax.figure
    probe = ax.text(0, 0, "lp", fontsize=size, family=family, fontweight=weight)
    _, h, d = fig.canvas.get_renderer().get_text_width_height_descent(
        "lp", probe.get_fontproperties(), ismath=False)
    probe.remove()
    return (h / 2 - d) / (fig.dpi / 100)


def arrow(ax, pts, label=None, label_xy=None):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys, color=LINE, lw=1.4, zorder=1, solid_capstyle="round")
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.4, mutation_scale=13))
    if label:
        lx, ly = label_xy
        ax.text(lx, ly, label, fontsize=10.2, color=GREY, va="center")


def fig1():
    W, H, D = 1340, 1126, 86
    fig, ax = canvas(W, H, "The agent calls 5 MCP tools that wrap a knowledge graph and a vector index")
    box(ax, 64, 100, 1216, 100, "Agent",
        [("your own loop (labs/lab8: THINK \u2192 TOOL_USE \u2192 OBSERVE \u2192 END_TURN), Claude Desktop, LangFlow \u2014 any MCP client."
          "  The agent\u2019s own LLM writes the answer.", GREY)])
    arrow(ax, [(672, 200), (672, 262)], "MCP streamable-http \u00b7 tools/list \u2192 tools/call", (694, 231))
    box(ax, 64, 262, 1216, 156 + D, "MCP Server \u00b7 FastMCP \u00b7 port 8100 \u00b7 5 tools, each reaches the engine differently",
        ["search_pdpa \u2192 keyword LLM + vector index (profiles, chunks) + graph BFS \u2014 the pipeline of the search figure",
         "get_related_sections \u2192 knowledge graph only: edges in and out of one node",
         "get_penalty \u2192 knowledge graph only: BFS from a section to Penalty nodes",
         "get_section_text \u2192 statute text by section id, read from the Markdown \u00b7 get_pdpa_summary \u2192 counts by node and edge type",
         ("only search_pdpa uses the LLM and vector search; the other four read the graph or statute text directly", GREY),
         ("stateless_http=True \u00b7 each tool\u2019s docstring is the description the agent reads before choosing a tool", GREY)])
    arrow(ax, [(672, 418 + D), (672, 474 + D)], "search \u00b7 traverse \u00b7 read section text", (694, 447 + D))
    box(ax, 64, 474 + D, 1216, 330, "PDPA LightRAG Engine \u00b7 lightrag/", [], fill=PANEL)
    ax.text(446, 508 + D, "this repo\u2019s own code, following the LightRAG approach (not the LightRAG library)",
            fontsize=10.2, color=GREY, va="center", zorder=3)
    box(ax, 92, 545 + D, 566, 186, "Knowledge Graph \u00b7 NetworkX (in-memory)",
        ["190 nodes \u00b7 382 edges",
         "11 node types \u00b7 26 edge types",
         "search_pdpa: BFS 2 hops from \u2264 3 seeds, both directions",
         "get_penalty: reports penalties within 2 hops"], fill=BLUE_FILL, edge=BLUE_EDGE, lw=2.2)
    box(ax, 686, 545 + D, 566, 186, "Vector Index \u00b7 BGE-M3 + Qdrant \u00b7 used by search_pdpa only",
        ["dense 1024-d + sparse (lexical weights)",
         "pdpa_profiles 572 = 190 node + 382 edge profiles",
         "pdpa_chunks 96 = full text, one per section",
         "hybrid search \u2192 RRF fusion (k = 60)"], title_size=11.6)
    ax.text(86, 770 + D, "LLM (OpenRouter \u00b7 LLM_MODEL) only for keyword extraction in search_pdpa \u00b7 "
            "Qdrant 1.20.0 runs as a separate container", fontsize=10.4, color=GREY, va="center", zorder=3)
    arrow(ax, [(672, 804 + D), (672, 862 + D)],
          "loaded at startup only \u00b7 no hot-reload \u00b7 both collections rebuilt at every start", (694, 834 + D))
    box(ax, 64, 862 + D, 1216, 128, "Data layer \u00b7 ./data (folder mounted into the container)",
        ["pdpa_full_text_v2.md \u00b7 96 sections (H1 Act \u2192 H2 Chapter \u2192 H3 Part \u2192 H4 Section)",
         "pdpa_knowledge_graph.json \u00b7 190 nodes / 382 edges (generated by scripts/build_graph.py)"])
    fig.savefig(OUT / "fig1_architecture.png", facecolor="white"); plt.close(fig)


def fig3():
    # Box titles, arrow labels and the last box are English. The body lines of steps 1-6 are Thai so that
    # learners can read them. Copied from the running system: the question, the keyword kinds in the prompt,
    # the statute text in a graph line and the three context headers (retrieval.py). The example in step 1
    # ("ลายนิ้วมือ" -> "ข้อมูลชีวภาพ") follows the figure's question; it is not the example in the prompt.
    W, H = 1340, 1588
    fig, ax = canvas(W, H, "search_pdpa: one question, six steps, graph + statute text in one context")
    ax.text(64, 78, "the only one of the 5 MCP tools that uses the LLM and vector search — the other four look up the graph or the statute text directly",
            fontsize=10.2, color=GREY, va="center")
    box(ax, 268, 104, 808, 100, "User question (คำถามของผู้ใช้)",
        [("“บริษัทเก็บลายนิ้วมือพนักงานเพื่อลงเวลาทำงาน ต้องขอความยินยอมไหม”", GREY)], center=True)
    arrow(ax, [(672, 204), (672, 240)])
    box(ax, 208, 240, 928, 214, "1  LLM keyword extraction (LLM_MODEL via OpenRouter) — the only LLM call",
        ["low-level ≤ 8 คำ: คำเฉพาะเจาะจง เช่น ชื่อหน่วยงาน สิทธิเฉพาะ หน้าที่เฉพาะ บทลงโทษ",
         "high-level ≤ 6 คำ: คำกว้าง เช่น หลักการ หมวดหมู่ แนวคิด ขั้นตอน",
         "ใช้ถ้อยคำแบบที่ตัวบทใช้ เช่น “ลายนิ้วมือ” → “ข้อมูลชีวภาพ”",
         "ใส่เลขมาตราเฉพาะเมื่อคำถามระบุมาเอง หรือมั่นใจว่าตรงประเด็น ไม่เกิน 2 มาตรา",
         ("จากนั้นโค้ดต่อคำของแต่ละชุดเป็นข้อความค้น 1 ข้อความ (low 1 ข้อความ high 1 ข้อความ)", GREY)])
    arrow(ax, [(672, 454), (672, 482), (346, 482), (346, 510)])
    arrow(ax, [(672, 482), (996, 482), (996, 510)])
    box(ax, 64, 510, 566, 186, "2  Profile search · pdpa_profiles (572)",
        ["รอบ A: คำค้น high-level → 5 อันดับแรก (top_k)",
         "รอบ B: คำค้น low-level → 3 อันดับแรก",
         "แต่ละรอบ: dense + sparse → RRF (k = 60)",
         ("รวมผล: รอบ A ก่อน แล้วต่อด้วยผลรอบ B ที่ไม่ซ้ำ (รวม ≤ 8)", GREY)])
    box(ax, 714, 510, 566, 186, "5  Chunk search · pdpa_chunks (96)",
        ["รวมคีย์เวิร์ด low + high เป็นคำค้นเดียว",
         "dense + sparse → RRF (k = 60)",
         "ได้ตัวบทเต็มของมาตรา ≤ 5 มาตรา",
         ("ไม่ขึ้นกับขั้นที่ 3–4: ไม่ใช้กราฟ", GREY)])
    arrow(ax, [(346, 696), (346, 740)], "profile ids (node or edge profiles)", (366, 718))
    box(ax, 64, 740, 566, 158, "3  Pick seeds — no LLM",
        ["ไล่ดูรายการที่รวมแล้วทีละรายการตามลำดับ",
         "ข้าม edge profile (id มี “--”) และโหนดตัว พ.ร.บ.",
         "3 โหนดแรกที่ผ่านเงื่อนไข = seed เช่น def_biometric"])
    arrow(ax, [(346, 898), (346, 942)], "≤ 3 seed nodes", (366, 920))
    box(ax, 64, 942, 566, 272, "4  Multi-hop BFS · NetworkX",
        ["เดิน 2 hop จาก seed แต่ละตัว ทั้งเส้นขาเข้าและขาออก",
         "เก็บ ≤ 15 บรรทัด แบ่งให้ seed ทุกตัวเท่ากัน วนทีละ seed",
         "ลำดับ: เส้นบทลงโทษและหน้าที่ก่อน ตามด้วยเส้นอ้างมาตรา",
         "และข้อยกเว้น แล้วเส้นชนิดอื่น เส้นโครงสร้างอยู่ท้ายสุด",
         ("ถ้าถามเรื่องโทษ: มาตราโทษที่อ้างมายังโหนดนั้นขึ้นก่อน", GREY),
         "[hop1] def_biometric ←DEFINES— sec_26: #### มาตรา ๒๖ ห้ามมิให้…",
         "[hop2] sec_26 —GRANTS_EXEMPTION→ sec26_ex1: …"],
        fill=BLUE_FILL, edge=BLUE_EDGE, lw=2.2, mono=(6,))
    arrow(ax, [(346, 1214), (346, 1244), (530, 1244), (530, 1274)])
    arrow(ax, [(996, 696), (996, 1244), (814, 1244), (814, 1274)], "full section text", (1014, 968))
    box(ax, 248, 1274, 848, 158, "6  Build hybrid context — 3 หัวข้อใน context",
        ["## ความรู้จาก Knowledge Graph (PDPA) — ข้อความของ profile ≤ 8 รายการ (จากขั้นที่ 2)",
         "### ข้อมูลเชื่อมโยง (multi-hop graph): — ผลเดินกราฟ ≤ 15 บรรทัด (จากขั้นที่ 4)",
         "## เนื้อหาต้นฉบับ PDPA (Original Text) — ตัวบทเต็ม ≤ 5 มาตรา (จากขั้นที่ 5)"])
    arrow(ax, [(672, 1432), (672, 1464)])
    box(ax, 318, 1464, 708, 84, "JSON back to the agent",
        [("the server retrieves · the agent’s LLM reads and answers (lab8 answers in Thai)", GREY)], center=True)
    fig.savefig(OUT / "fig3_search_pipeline.png", facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    fig1(); fig3()
    print("wrote", OUT / "fig1_architecture.png", "and", OUT / "fig3_search_pipeline.png")
