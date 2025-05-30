from core.tokenizer import count_tokens
import nltk

def smart_chunk(text, max_tokens=200):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        temp_chunk = current_chunk + " " + sentence if current_chunk else sentence
        if count_tokens(temp_chunk) <= max_tokens:
            current_chunk = temp_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
