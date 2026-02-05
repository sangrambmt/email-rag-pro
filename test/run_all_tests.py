import subprocess
import sys

tests = [
    "test\\test_api.py",
    "test\\load_sample_data.py",
    "test\\test_document_formats.py",
    "test\\test_chunking.py",
    "test\\test_full_pipeline.py",
    "test\\test_edge_cases.py",
]

print("Running all tests...\n")

for i, test in enumerate(tests, 1):
    print(f"\n[{i}/{len(tests)}] Running {test}...")
    result = subprocess.run([sys.executable, test])
    print("✅ Passed" if result.returncode == 0 else "❌ Failed")

print("\n✅ All tests completed!")