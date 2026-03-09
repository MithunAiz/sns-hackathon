import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
try:
    with open('models_utf8.txt', 'w', encoding='utf-8') as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(m.name + '\n')
except Exception as e:
    with open('models_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}\n")
