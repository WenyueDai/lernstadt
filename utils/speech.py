import asyncio
import edge_tts
import re

async def generate_speech(text, voice, filename="voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def clean_text_for_tts(text: str) -> str:
    text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)  # remove *bold* or **bold**
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)     # remove _italic_ or __italic__
    text = re.sub(r"\([^)]*\)", "", text)                 # remove parentheticals (like this)
    return text.strip()

def run_speech(text, voice, filename="voice.mp3"):
    clean_text = clean_text_for_tts(text)
    communicate = edge_tts.Communicate(clean_text, voice)
    asyncio.run(communicate.save(filename))
