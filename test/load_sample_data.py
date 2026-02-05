from pathlib import Path

EMAIL_DIR = Path("data/emails")
EMAIL_DIR.mkdir(parents=True, exist_ok=True)

emails = {
    "01_pricing.txt": "Subject: Pricing\nAnnual: $50,000/year\nDiscount: 20% for 3-year",
    "02_contract.txt": "Payment terms: 30-day\nGo-live: Feb 15, 2025\nSupport: 24/7 included",
    "03_issue.txt": "URGENT: SSO failing\nError: Invalid SAML\nPriority: HIGH",
    "04_resolved.txt": "Issue resolved\nRoot cause: Certificate mismatch\nStatus: Fixed",
}

print("Loading sample data...\n")

for name, content in emails.items():
    (EMAIL_DIR / name).write_text(content)
    print(f"✅ {name}")

print("\n✅ Sample data loaded!")
print("\nTry these queries:")
print("- What is the annual price?")
print("- What is the go-live date?")
print("- What issue was escalated?")