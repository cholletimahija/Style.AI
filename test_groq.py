import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ API key not found. Check your .env file.")
    exit()

print("✅ API key loaded successfully!")

# Initialize Groq client
client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say hello like a fashion stylist."}
        ],
        max_tokens=50
    )

    print("\n🎉 Groq API is working!")
    print("Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ Error connecting to Groq API:")
    print(e)