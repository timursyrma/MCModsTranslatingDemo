import requests
import json
import time

def translate_text(text):
    url = "http://localhost:11434/api/generate"
    prompt = (
        "Translate Minecraft mod text from English to Russian.\n"
        "Keep technical identifiers unchanged.\n"
        f"Text: {text}"
    )
    
    payload = {
        "model": "qwen2.5:latest",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

        for line in content.split('\n'):
            if translated := translate_text(line):
                print(f"Translation:\n{translated}\n")
            else:
                print("Translation failed")

if __name__ == "__main__":
    process_file('en_us.lang')

