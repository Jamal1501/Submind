import nltk
nltk.download('punkt')

from core.memory import MemoryEngine
from core.token_filter import filter_by_token_limit
from storage.store import save_memory, load_memory

# Setup
mem = MemoryEngine()

# Add some fake memory entries
mem.add("The sky is blue.")
mem.add("The AI layer should optimize context injection.")
mem.add("Long-term scoring is needed for memory relevance.")

# Save and reload
save_memory(mem.get_all())
loaded = load_memory()

# Filter based on token budget
filtered = filter_by_token_limit(mem.get_all(), max_tokens=30)

print("Filtered memory:")
for entry in filtered:
    print("-", entry.text)
