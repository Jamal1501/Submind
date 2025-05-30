import time
from core.chunker import smart_chunk

class MemoryEntry:
    def __init__(self, text, score=0.0, created_at=None, usage_count=0, tags=None):
        self.text = text
        self.score = score
        self.created_at = created_at or time.time()
        self.usage_count = usage_count
        self.tags = tags or []
        self.relevance_score = 0.5

class MemoryEngine:
    def __init__(self, max_chunk_tokens=200):
        self.memory = []
        self.max_chunk_tokens = max_chunk_tokens

    def add(self, text, tags=None):
        chunks = smart_chunk(text, max_tokens=self.max_chunk_tokens)
        for chunk in chunks:
            entry = MemoryEntry(chunk, tags=tags)
            entry.engine = self
            self.memory.append(entry)

    def get_all(self):
        return self.memory

    def clear(self):
        self.memory = []

    def update_memory_score(self, entry, relevance_factor=0.2, decay_rate=0.01, min_score=0.05, tag_boost=0.1, important_tags=None):
        if important_tags is None:
            important_tags = []

        entry.usage_count += 1
        time_elapsed = (time.time() - entry.created_at) / 60
        decay = decay_rate * time_elapsed

        entry.relevance_score += relevance_factor
        if any(tag in entry.tags for tag in important_tags):
            entry.relevance_score += tag_boost

        entry.score = max(min_score, entry.relevance_score - decay)

    def retrieve(self, top_k=5):
        return sorted(self.memory, key=lambda x: (x.score, x.created_at), reverse=True)[:top_k]

    def update_scores(self):
        for entry in self.memory:
            self.update_memory_score(entry, important_tags=["goal", "user_pref", "priority"])

# 🔧 Simple global engine (optional)
engine = MemoryEngine()

def save_memory(text, tags=None, importance=None):
    """
    Adds memory with optional tags and importance override.
    """
    engine.add(text, tags=tags)
    if importance:
        for entry in engine.memory[-1:]:
            entry.relevance_score = importance
            entry.score = importance
