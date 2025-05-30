from core.memory import MemoryEngine
from core.chunker import smart_chunk
from core.injector import inject_memory as inject_memory_new
from storage.store import save_memory, load_memory
import time
from core.semantic_score import calculate_semantic_similarity

def normalize_scores(memory_entries):
    # Normalize the scores of memories by adjusting for their age
    current_time = time.time()
    for entry in memory_entries:
        age = current_time - entry.created_at
        decay_factor = 0.99 ** (age / 3600)  # Decay per hour, adjust as needed
        entry.score *= decay_factor  # Apply decay to the score

    return memory_entries

def main():
    # Initialize the memory engine
    memory = MemoryEngine()

    # Define important tags that should boost relevance
    important_tags = ["goal", "priority", "user_pref"]

    # Example entries with and without tags
    entries = [
        ("OpenAI develops artificial intelligence for the benefit of humanity.", ["tech"]),
        ("Token efficiency and relevance scoring are crucial to optimize memory use across contexts.", ["priority"]),
        ("This memory contains a core user preference.", ["user_pref"]),
        ("This is just some unrelated trivia.", ["trivia"]),
        ("Remember to focus on building Submind into a working system.", ["goal"]),
    ]

    # Add chunks to memory
    for text, tags in entries:
        chunks = smart_chunk(text, max_tokens=30)
        for chunk in chunks:
            memory.add(chunk, tags=tags)

    # Update scores with tag boosting
    for entry in memory.get_all():
        memory.update_memory_score(entry, important_tags=important_tags)

    # Save to SQLite database
    save_memory(memory.get_all())

    # Load the memory entries back from SQLite
    loaded_entries = load_memory()

    # Normalize scores (apply age-based decay)
    loaded_entries = normalize_scores(loaded_entries)

    # Prepare a prompt for injection
    user_prompt = "Why is token efficiency important in AI?"

    # Inject memory into prompt
    injected = inject_memory_new(user_prompt, top_k=5)

    print("\n--- Injected Prompt ---\n")
    print(injected)

    # Optionally, print out loaded entries for verification
    print("\n--- Loaded Memory Entries ---\n")
    for entry in loaded_entries:
        print(f"Text: {entry.text} | Score: {entry.score:.2f} | Created At: {entry.created_at} | Usage Count: {entry.usage_count} | Tags: {entry.tags}")



if __name__ == "__main__":
    main()

import sys
sys.path.append(".")

from storage.store import backfill_text_hashes

backfill_text_hashes()  # Fills missing text_hash fields
