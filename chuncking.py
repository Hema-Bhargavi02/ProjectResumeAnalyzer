import tiktoken

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

encoding = tiktoken.get_encoding("cl100k_base")


def chunkText(text):
    if not text or not text.strip():
        return []

    tokens = encoding.encode(text)
    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP

    for start in range(0, len(tokens), step):
        end = min(start + CHUNK_SIZE, len(tokens))
        chunk = encoding.decode(tokens[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end == len(tokens):
            break

    return chunks
