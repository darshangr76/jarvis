# JARVIS — Local Voice AI Assistant

A JARVIS-style voice assistant running entirely on macOS.

## Features
- Local LLM (Qwen 2.5 Coder via Ollama)
- JARVIS personality
- Voice output (macOS `say`)
- Open Mac apps
- Play music on YouTube
- Google search
- Real time and date
- Conversation memory

## Setup

python3.12 -m venv ~/jarvis-env
source ~/jarvis-env/bin/activate
pip install anyrobo ollama
ollama pull qwen2.5-coder:3b

## Run

source ~/jarvis-env/bin/activate
python jarvis.py

## Commands

| Say | JARVIS does |
|---|---|
| Open Safari | Launch app |
| Play hotel california | YouTube search |
| Play music | YouTube Music |
| Search coffee shops | Google search |
| What time is it? | Speaks time |
| quit | Exit |

## License
MIT
