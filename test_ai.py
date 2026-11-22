import streamlit as st
from google import genai

print("Connecting to NEXUS AI...", flush=True)

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say Hello to NEXUS AI."
)

print("\nGemini Response:", flush=True)
print(response.text, flush=True)