import os
print("Starting simple test...")

# Test environment variable loading
print("Testing environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv("../.env")
    api_key = os.getenv('GOOGLE_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key (first 10 chars): {api_key[:10]}...")
except Exception as e:
    print(f"Error loading env: {e}")

# Test Google AI import
print("\nTesting Google AI import...")
try:
    import google.generativeai as genai
    print("Google AI imported successfully!")
except Exception as e:
    print(f"Error importing Google AI: {e}")

print("\nSimple test completed!")
