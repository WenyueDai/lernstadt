# Deutsch Town – NPC Dialogue Engine

## Introduction

This project is a **German-language NPC interaction engine** powered by **Streamlit**, **spaCy**, **Edge TTS**, and **LLMs via OpenRouter**.  
It simulates dynamic NPC conversations with evolving trust, gossip exchange, daily moods, speech synthesis, and multilingual support.

---

## Features

- Interactive NPC dialogue (trust, mood, suspicion)  
  → NPCs have personalities, gossip pools, and evolving trust levels based on player interaction.
- Natural language understanding via **spaCy**
- Text-to-speech using **Edge TTS**
- Uses **`deepseek/deepseek-chat-v3-0324:free`** through **OpenRouter API**
- Conversation summaries and memory stored for each NPC

---

## Installation

### 1. Clone the repository and create environment

```bash
git clone https://github.com/yourname/deutsch-town-npc.git
cd deutsch-town-npc
conda create -n lernstadt python=3.10 -y
conda activate lernstadt
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install German spaCy NLP model

```bash
python -m spacy download de_core_news_sm
```

### 4. Set up your OpenRouter API key

- Go to [https://openrouter.ai](https://openrouter.ai)
- Sign up and obtain your free API key
- Save it in a plain text file named `openai_key.txt` in the root directory

The script will automatically read this key on startup.

### 5. Run the app

```bash
./clean_streamlit.sh
```

Or manually:

```bash
streamlit run main.py --server.headless true
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Folder Structure

```
.
├── main.py                  # Main Streamlit app
├── openai_key.txt           # API key for OpenRouter
├── jpg/                     # NPC & scene images
├── role_json/               # NPC and gossip definitions
├── utils/                   # All helper modules
├── voice.mp3                # Synthesized output
├── requirements.txt         # Dependencies
```

---

## Tips

-  Modify `MODEL_NAME` in `main.py` if you want to use another model
-  To prevent the browser from auto-opening, use:
  ```bash
  streamlit run main.py --server.headless true
  ```
- You can support multiple keys (OpenAI, Groq, etc.) by expanding the `load_openrouter_key()` function

---

## License

MIT License. Free to use and modify.