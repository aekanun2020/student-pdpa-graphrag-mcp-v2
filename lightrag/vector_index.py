"""
Vector Index — BGE-M3 (Dense + Sparse) + Qdrant (PDPA RAG version)
==================================================================
มี 2 collection: profiles ของ knowledge graph และ chunks ของตัวบท
"""

import os
import uuid
from FlagEmbedding import BGEM3FlagModel
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, SparseVectorParams, SparseIndexParams,
    Distance, PointStruct, SparseVector,
    Prefetch, FusionQuery, Fusion,
)

try:  # qdrant-client >= 1.16 — RRF ที่กำหนดค่า k ได้
    from qdrant_client.models import RrfQuery, Rrf
except ImportError:  # client เก่า: ใช้ Fusion.RRF (k ตามค่า default ของ Qdrant = 2)
    RrfQuery = Rrf = None

PROFILE_COLLECTION = "pdpa_profiles"
CHUNK_COLLECTION = "pdpa_chunks"
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))

# RRF: score(d) = Σ 1 / (k + rank)  — k=60 ตาม paper ต้นฉบับของ RRF (Cormack et al., 2009)
# Qdrant ใช้ k=2 ถ้าไม่ระบุ; ตั้ง RRF_K=0 เพื่อกลับไปใช้ค่า default ของ Qdrant
RRF_K = int(os.environ.get("RRF_K", "60"))

# BGE-M3 รับได้ถึง 8192 tokens; มาตราที่ยาวที่สุด (ม.26) = 810 tokens
# ค่าเดิม 512 ทำให้ 7 มาตราถูกตัดท้ายตอน embed
CHUNK_MAX_LENGTH = int(os.environ.get("CHUNK_MAX_LENGTH", "1024"))


class VectorIndex:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        print(f"  Loading BGE-M3 model...")
        self.model = BGEM3FlagModel(model_name, use_fp16=True)
        self.dim = 1024
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        self.profiles = []
        self.chunk_store = {}
        self._rrf_k_ok = RRF_K > 0 and RrfQuery is not None

    def _embed(self, texts: list[str], max_length: int = 512) -> dict:
        result = self.model.encode(
            texts, batch_size=32, max_length=max_length,
            return_dense=True, return_sparse=True,
        )
        return {"dense": result["dense_vecs"], "sparse": result["lexical_weights"]}

    def _hybrid_query(self, collection: str, dense_vec, sparse_vec, top_k: int, id_key: str) -> list:
        """Dense + sparse prefetch แล้วรวมอันดับด้วย RRF — คืน list ของ points (top_k)

        k: ใช้ RRF_K เมื่อ client และ server รองรับ (Qdrant >= 1.16) ถ้าไม่รองรับจะถอยไปใช้
        Fusion.RRF ซึ่ง k เป็นค่า default ของ Qdrant (2) และแจ้งเตือนครั้งเดียว

        ลำดับคงที่: RRF ให้คะแนนจากอันดับ จึงมีคะแนนเท่ากันบ่อย (เช่น อันดับ 3 ฝั่ง dense กับ
        อันดับ 3 ฝั่ง sparse) และ Qdrant ไม่รับประกันลำดับของคะแนนที่เท่ากัน — คำค้นเดิมจึงได้
        seed ต่างกันในแต่ละครั้ง จึงขอผลรวมทั้งหมดของสอง prefetch (ไม่เกิน 4 * top_k)
        แล้วเรียงเองด้วย (คะแนน, id) ก่อนตัด top_k
        """
        prefetch = [
            Prefetch(query=dense_vec.tolist(), using="dense", limit=top_k * 2),
            Prefetch(query=sparse_vec, using="sparse", limit=top_k * 2),
        ]
        fetch = top_k * 4
        results = None
        if self._rrf_k_ok:
            try:
                results = self.client.query_points(
                    collection_name=collection, prefetch=prefetch,
                    query=RrfQuery(rrf=Rrf(k=RRF_K)), limit=fetch,
                )
            except Exception as e:  # server เก่ากว่า 1.16 ไม่รู้จัก query แบบ rrf
                self._rrf_k_ok = False
                print(f"  ⚠️ RRF k={RRF_K} ใช้ไม่ได้ ({type(e).__name__}) — ใช้ค่า default ของ Qdrant (k=2) แทน")
        if results is None:
            results = self.client.query_points(
                collection_name=collection, prefetch=prefetch,
                query=FusionQuery(fusion=Fusion.RRF), limit=fetch,
            )
        points = sorted(results.points,
                        key=lambda pt: (-round(pt.score, 9), str(pt.payload.get(id_key, ""))))
        return points[:top_k]

    @staticmethod
    def _to_sparse_vector(lexical_weights: dict) -> SparseVector:
        indices, values = [], []
        for token_id, weight in lexical_weights.items():
            indices.append(int(token_id))
            values.append(float(weight))
        return SparseVector(indices=indices, values=values)

    @staticmethod
    def _keys_to_text(profile: dict) -> str:
        keys = profile.get("keys", [])
        return " ".join(str(k) for k in keys if k and str(k).strip())

    # ─── Profile Index ────────────────────────────────────────

    def build_profiles(self, profiles: list[dict]):
        """embed knowledge graph profiles แล้ว upsert เข้า Qdrant"""
        self.profiles = profiles

        if self.client.collection_exists(PROFILE_COLLECTION):
            self.client.delete_collection(PROFILE_COLLECTION)

        self.client.create_collection(
            collection_name=PROFILE_COLLECTION,
            vectors_config={
                "dense": VectorParams(size=self.dim, distance=Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": SparseVectorParams(index=SparseIndexParams(on_disk=False)),
            },
        )

        texts = [self._keys_to_text(p) for p in profiles]
        print(f"  Embedding {len(texts)} profiles (keys only)...")
        embeddings = self._embed(texts)

        points = []
        for i, p in enumerate(profiles):
            dense_vec = embeddings["dense"][i]
            sparse_vec = self._to_sparse_vector(embeddings["sparse"][i])
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector={"dense": dense_vec.tolist(), "sparse": sparse_vec},
                payload={
                    "index": i,
                    "profile_id": p.get("id", ""),
                    "node_category": p.get("node_category", ""),
                },
            ))

        batch_size = 500
        for start in range(0, len(points), batch_size):
            batch = points[start:start + batch_size]
            self.client.upsert(collection_name=PROFILE_COLLECTION, points=batch)

        print(f"  ✅ Upserted {len(points)} profile vectors to Qdrant ({QDRANT_HOST}:{QDRANT_PORT})")

    def search_profiles(self, query: str, top_k: int = 10) -> list[dict]:
        embeddings = self._embed([query])
        dense_vec = embeddings["dense"][0]
        sparse_vec = self._to_sparse_vector(embeddings["sparse"][0])

        points = self._hybrid_query(PROFILE_COLLECTION, dense_vec, sparse_vec, top_k, id_key="profile_id")

        output = []
        for point in points:
            idx = point.payload.get("index", 0)
            if idx < len(self.profiles):
                output.append({"profile": self.profiles[idx], "score": point.score})
        return output

    # ─── Chunk Index ──────────────────────────────────────────

    def build_chunks(self, chunk_store: dict):
        """embed มาตรา chunks แล้ว upsert เข้า Qdrant"""
        self.chunk_store = chunk_store

        if not chunk_store:
            print("  ⚠️ chunk_store ว่าง — ข้าม build_chunks")
            return

        if self.client.collection_exists(CHUNK_COLLECTION):
            self.client.delete_collection(CHUNK_COLLECTION)

        self.client.create_collection(
            collection_name=CHUNK_COLLECTION,
            vectors_config={
                "dense": VectorParams(size=self.dim, distance=Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": SparseVectorParams(index=SparseIndexParams(on_disk=False)),
            },
        )

        chunk_ids = sorted(chunk_store.keys())
        texts = [chunk_store[cid]["text"] for cid in chunk_ids]
        print(f"  Embedding {len(texts)} chunks (full text)...")
        embeddings = self._embed(texts, max_length=CHUNK_MAX_LENGTH)

        points = []
        for i, cid in enumerate(chunk_ids):
            chunk = chunk_store[cid]
            dense_vec = embeddings["dense"][i]
            sparse_vec = self._to_sparse_vector(embeddings["sparse"][i])
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector={"dense": dense_vec.tolist(), "sparse": sparse_vec},
                payload={
                    "chunk_id": cid,
                    "section_id": chunk.get("section_id", ""),
                    "header_2": chunk.get("header_2", ""),
                    "header_3": chunk.get("header_3", ""),
                },
            ))

        batch_size = 500
        for start in range(0, len(points), batch_size):
            batch = points[start:start + batch_size]
            self.client.upsert(collection_name=CHUNK_COLLECTION, points=batch)

        print(f"  ✅ Upserted {len(points)} chunk vectors to Qdrant '{CHUNK_COLLECTION}'")

    def search_chunks(self, query: str, top_k: int = 5) -> list[dict]:
        """ค้นหาเนื้อหามาตรา PDPA จาก Qdrant"""
        if not self.client.collection_exists(CHUNK_COLLECTION):
            return []

        embeddings = self._embed([query])
        dense_vec = embeddings["dense"][0]
        sparse_vec = self._to_sparse_vector(embeddings["sparse"][0])

        points = self._hybrid_query(CHUNK_COLLECTION, dense_vec, sparse_vec, top_k, id_key="chunk_id")

        output = []
        for point in points:
            cid = point.payload.get("chunk_id", "")
            chunk_data = self.chunk_store.get(cid, {})
            output.append({
                "chunk_id": cid,
                "text": chunk_data.get("text", ""),
                "section_id": point.payload.get("section_id", ""),
                "header_2": point.payload.get("header_2", ""),
                "header_3": point.payload.get("header_3", ""),
                "score": point.score,
            })
        return output
