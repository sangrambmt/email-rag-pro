import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

print("=" * 50)
print("OpenAI API Key Test")
print("=" * 50)

# Check if API key exists
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
    print("\nPlease add this to your .env file:")
    print("OPENAI_API_KEY=sk-your-key-here")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Test API connection
print("\n🔄 Testing API connection...")

try:
    from openai import OpenAI
    
    # Create client without proxies argument
    client = OpenAI(api_key=api_key)
    
    # Simple test call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'API key is working!' if you can read this."}
        ],
        max_tokens=20
    )
    
    answer = response.choices[0].message.content
    
    print("✅ API Connection Successful!")
    print(f"✅ Response: {answer}")
    print("\n" + "=" * 50)
    print("Your OpenAI API key is working correctly! ✅")
    print("=" * 50)

except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("\nTry running: python -m pip install --upgrade openai")
    
except TypeError as e:
    print(f"❌ Version Error: {str(e)}")
    print("\nYour OpenAI library version is incompatible.")
    print("Run: python -m pip install --upgrade openai")

except Exception as e:
    error_msg = str(e)
    print(f"❌ API Connection Failed!")
    print(f"❌ Error: {error_msg}")
    
    if "401" in error_msg or "Incorrect API key" in error_msg:
        print("\n🔴 Issue: Invalid API Key")
        print("Fix: Check your API key at https://platform.openai.com/api-keys")
    elif "429" in error_msg or "quota" in error_msg.lower():
        print("\n🔴 Issue: No credits/quota remaining")
        print("Fix: Add credits at https://platform.openai.com/account/billing")
    elif "403" in error_msg:
        print("\n🔴 Issue: API key doesn't have permission")
        print("Fix: Check your organization settings")
    else:
        print("\nPossible issues:")
        print("1. Network connection problem")
        print("2. Firewall blocking requests")
        print("3. Proxy configuration needed")