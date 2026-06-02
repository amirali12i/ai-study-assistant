import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODELS = [
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openai/gpt-oss-120b:free",
]

system_prompt = "You are a helpful study assistant for university students. Only answer academic questions related to subjects like math, programming, physics, and computer science. Be clear and educational in your responses."

history = [{"role": "system", "content": system_prompt}]

def ask(user_input):
    history.append({"role": "user", "content": user_input})
    for model in MODELS:
        response = requests.post(API_URL, headers=headers, json={
            "model": model,
            "messages": history
        })
        data = response.json()
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": reply})
            return reply
    history.pop()
    return "⚠️ All models are busy right now. Please try again in a moment."

print("🤖 AI Study Assistant")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    print(f"🤖: {ask(user_input)}\n")