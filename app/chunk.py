def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + max_chars, length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        start = start + max_chars - overlap
        
        if start >= length:
            break

    return chunks