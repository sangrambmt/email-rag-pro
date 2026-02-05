from app.chunk import chunk_text

tests = [
    ("Short text", "This is short.", 1),
    ("Long text", "A" * 2000, 2),
    ("Empty text", "", 1),
    ("Exact max", "X" * 1000, 1),
]

print("Testing chunking logic...\n")

for name, text, expected in tests:
    chunks = chunk_text(text)
    result = "✅" if len(chunks) >= expected else "❌"
    print(f"{result} {name}: {len(chunks)} chunks (expected ≥{expected})")

print("\n✅ Chunking tests complete!")