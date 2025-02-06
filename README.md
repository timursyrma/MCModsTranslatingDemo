# Ollama Docker Setup with NVIDIA GPU Support

This guide will help you set up Ollama with NVIDIA GPU support using Docker.

## Prerequisites

- Docker installed
- NVIDIA GPU
- Linux system (Arch Linux in this example)

## 1. Install and Configure NVIDIA Container Toolkit

First, install the NVIDIA Container Toolkit:
```bash
sudo pacman -S nvidia-container-toolkit
```

Configure Docker to use NVIDIA runtime:
```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

Restart Docker service to apply changes:
```bash
sudo systemctl restart docker
```

## 2. Create Docker Compose Configuration

Create a `docker-compose.yml` file with the following content:
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    runtime: nvidia
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 3. Start Ollama Container

Run the container in detached mode:
```bash
docker-compose up -d
```

## 4. Verify NVIDIA GPU Support

Check if the GPU is properly recognized:
```bash
docker exec -it ollama nvidia-smi
```

## 5. Working with Models

### Pull a Model
```bash
docker exec -it ollama ollama pull qwen2.5
```

### List Installed Models
```bash
curl http://localhost:11434/api/tags
```

## 6. Example Usage: Translation Script

Here's an example Python script (`translate.py`) that uses Ollama for translation:
```python
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
```

Run the translation script:
```bash
./myvenv/bin/python translate.py
```
