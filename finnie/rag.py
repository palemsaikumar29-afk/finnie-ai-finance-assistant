"""RAG over the finance knowledge base (FAISS + sentence-transformers)."""
from __future__ import annotations

import asyncio
from pathlib import Path

import faiss
import numpy as np

from finnie.config import settings

KB_DIR = Path(__file__).parent / "knowledge"
INDEX_PATH = KB_DIR / "index.faiss"


class KnowledgeBase:
    def __init__(self) -> None:
        self._model = None
        self._index = None
        self._docs: list[dict] = []

    # -- lazy, thread-safe-ish init --------------------------------------
    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return self._model

    def _load_docs(self) -> None:
        self._docs = []
        for path in sorted(KB_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            title = lines[0].lstrip("# ").strip() if lines else path.stem
            self._docs.append(
                {"id": path.stem, "title": title, "text": text.strip()}
            )

    def build(self) -> None:
        """Embed all articles and write the FAISS index (excluded from git)."""
        model = self._ensure_model()
        self._load_docs()
        if not self._docs:
            raise RuntimeError(f"No articles found in {KB_DIR}")
        texts = [d["text"] for d in self._docs]
        embs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        embs = np.asarray(embs, dtype=np.float32)
        index = faiss.IndexFlatIP(embs.shape[1])
        index.add(embs)
        faiss.write_index(index, str(INDEX_PATH))
        self._index = index

    def _ensure_index(self):
        if self._index is None:
            if INDEX_PATH.exists():
                self._index = faiss.read_index(str(INDEX_PATH))
                self._load_docs()
            else:
                self.build()
        return self._index

    def retrieve(self, query: str, k: int | None = None) -> list[dict]:
        index = self._ensure_index()
        model = self._ensure_model()
        k = k or settings.RAG_TOP_K
        q = np.asarray(
            model.encode([query], normalize_embeddings=True), dtype=np.float32
        )
        scores, ids = index.search(q, min(k, len(self._docs)))
        return [
            {**self._docs[i], "score": float(scores[0][n])}
            for n, i in enumerate(ids[0])
            if 0 <= i < len(self._docs)
        ]

    async def aretrieve(self, query: str, k: int | None = None) -> list[dict]:
        return await asyncio.to_thread(self.retrieve, query, k)


kb = KnowledgeBase()
