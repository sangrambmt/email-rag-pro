import requests
import time
from pathlib import Path

API_URL = "http://127.0.0.1:8000"
EMAIL_DIR = Path("data/emails")
EMAIL_DIR.mkdir(parents=True, exist_ok=True)

print("Testing Full Pipeline...\n")

# Check API
try:
    r = requests.get(f"{API_URL}/")
    print("✅ API running" if r.status_code == 200 else "❌ API error")
except:
    print("❌ API not reachable. Run: uvicorn app.main:app --reload")
    exit(1)

# Create test docs
docs = {
    "contract.txt": "Client: Acme Corp\nBudget: $50,000\nDeadline: June 30, 2025",
    "meeting.txt": "Next meeting: Feb 1st\nAttendees: John, Sarah, Mike",
}

for name, content in docs.items():
    (EMAIL_DIR / name).write_text(content)
    print(f"✅ Created {name}")

print("\nWaiting for indexing...")
time.sleep(3)

# Test queries
queries = [
    "What is the budget?",
    "When is the next meeting?",
]

for q in queries:
    r = requests.post(f"{API_URL}/ask", json={"question": q, "top_k": 3})
    data = r.json()
    print(f"\n❓ {q}")
    print(f"📝 {data['answer'][:80]}")
    print(f"📄 {data['sources']}")

print("\n✅ Pipeline test complete!")