import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")  # GPT-3.5/4

def count_tokens(text):
    return len(encoding.encode(text))
