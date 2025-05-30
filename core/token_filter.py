from core.tokenizer import count_tokens

def filter_by_token_limit(entries, max_tokens):
    selected = []
    total = 0
    for e in sorted(entries, key=lambda x: -e.score):
        tokens = count_tokens(e.text)
        if total + tokens > max_tokens:
            break
        selected.append(e)
        total += tokens
    return selected
