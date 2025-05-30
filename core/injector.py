import time
from core.tokenizer import count_tokens
from core.semantic_score import calculate_semantic_similarity

# New normalize_scores function
def normalize_scores(memory_entries, time_decay_factor=0.1, current_time=None):
    """
    Normalize memory scores over time so that older memories don't become irrelevant.
    """
    if current_time is None:
        current_time = time.time()  # Default to current time if not provided

    for entry in memory_entries:
        # Calculate the age of the memory (in seconds)
        age = current_time - entry.created_at
        
        # Apply a time decay to the score (lower score for older memories)
        # Time decay can be adjusted based on how quickly you want older memories to lose relevance
        time_decay_score = 1 / (1 + time_decay_factor * age)

        # Adjust score based on time decay
        entry.score *= time_decay_score

    return memory_entries
from core.semantic_score import calculate_semantic_similarity

def calculate_relevance_score(memory_text, prompt):
    """
    Calculate the relevance score of a memory entry based on semantic similarity to the user prompt.
    Debugging added to check similarity scores.

    Args:
    - memory_text (str): The text from memory to compare.
    - prompt (str): The user input prompt.

    Returns:
    - score (float): The relevance score based on cosine similarity.
    """
    # Get similarity scores between the memory text and the prompt
    similarity_scores = calculate_semantic_similarity([memory_text], prompt)

    # Debugging: Check the score
    print(f"Relevance score for memory: '{memory_text[:30]}...': {similarity_scores}")

    # Return the first score (since we only passed one memory_text)
    return similarity_scores[0] if similarity_scores else 0.0

def inject_memory(memory_entries, user_prompt, token_budget=500, score_threshold=0.08):
    # Simulate older memory for testing decay (remove this in production)
    for entry in memory_entries:
        entry.created_at -= 3600  # 1 hour ago

    # Update scores with decay if engine is attached
    if hasattr(memory_entries[0], "__class__") and hasattr(memory_entries[0], "engine"):
        memory_entries[0].engine.update_scores()
        for entry in memory_entries:
            print(f"[DEBUG] Text: {entry.text[:30]}... | Score: {entry.score:.2f} | Age: {(time.time() - entry.created_at)/60:.2f} min")

    # Calculate prompt similarity relevance using semantic scoring
    for entry in memory_entries:
        entry.score = calculate_relevance_score(entry.text, user_prompt)
        if hasattr(entry, "engine"):
            entry.engine.update_memory_score(entry)

    # Sort memory entries by score and recency (newer memories first)
    sorted_entries = sorted(memory_entries, key=lambda m: (m.score, m.created_at), reverse=True)

    injected = []
    total_tokens = 0

    # Loop through sorted entries and add them until the token budget is exhausted
    for entry in sorted_entries:
        if entry.score < score_threshold:  # Filter out low-relevance entries
            continue

        entry_tokens = count_tokens(entry.text)
        if total_tokens + entry_tokens > token_budget:
            break  # Stop when we hit the token budget

        # Add entry to injected prompt and update token count
        injected.append(entry.text)
        total_tokens += entry_tokens

    # Return the final injected prompt (combined entries)
    return "\n".join(injected)
