import requests

API_URL = "http://127.0.0.1:8000"

tests = [
    {"name": "Empty question", "payload": {"question": "", "top_k": 5}},
    {"name": "Long question", "payload": {"question": "What " * 50, "top_k": 5}},
    {"name": "Special chars", "payload": {"question": "Price? $$ @#", "top_k": 5}},
    {"name": "Large top_k", "payload": {"question": "test", "top_k": 100}},
    {"name": "File filter", "payload": {"question": "budget", "file_filter": "contract.txt"}},
]

print("Testing edge cases...\n")

for test in tests:
    try:
        r = requests.post(f"{API_URL}/ask", json=test["payload"], timeout=5)
        print(f"✅ {test['name']}: {r.status_code}")
    except Exception as e:
        print(f"❌ {test['name']}: {e}")

print("\n✅ Edge case tests complete!")