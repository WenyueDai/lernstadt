import streamlit as st
import os
import json
import datetime
import random
import re
from openai import OpenAI

from utils.ui_helpers import set_page
from utils.npc_tool import (
    load_npc, save_npc, update_trust, log_conversation,
    decay_trust, list_all_npcs, increase_suspicion
)
from utils.text_analysis import update_player_preferences, update_player_preferences_spacy
from utils.gossip_tool import share_gossip_with_others, filter_available_gossip
from utils.speech import run_speech
from utils.prompt_builder import build_npc_prompt
from utils.summary import generate_summary, generate_summaries_for_today
from utils.audio_tools import autoplay_audio
from utils.escape_tools import discover_escape_clues

# === Load API Key from File ===
def load_openrouter_key(path="openai_key.txt"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None

api_key = load_openrouter_key()
if not api_key:
    st.error("API key not found in openai_key.txt. Please create the file with your OpenRouter key.")
    st.stop()

# === Model Setup ===
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# === Session Setup ===
today, today_str, current_time_str = set_page()

scene_npcs = {
    "Café": ["anna"],
    "Hospital": ["lara"],
    "Street": ["jonas"]
}
scene_images = {
    "Café": "jpg/background_cafe.jpg",
    "Hospital": "jpg/background_hospital.jpg",
    "Street": "jpg/background_street.jpg"
}
npc_voices = {
    "anna": "de-DE-KatjaNeural",
    "lara": "de-DE-KatjaNeural",
    "jonas": "de-DE-ConradNeural"
}

# === Sidebar ===
scene = st.sidebar.selectbox("Ort", list(scene_npcs.keys()))
npc_name = st.sidebar.selectbox("Charakter", scene_npcs[scene])
npc_image = f"jpg/{npc_name.lower()}.jpg"
voice_name = npc_voices[npc_name]

# === Load NPC ===
npc, npc_file = load_npc(npc_name)
npc["name"] = npc_name
npc = update_trust(npc, today_str, npc.get("last_spoken", ""))
npc, decay_msg = decay_trust(npc, today_str, npc.get("last_spoken", ""))
if decay_msg:
    st.warning(f"{decay_msg}")

with open("role_json/gossip_pool.json", encoding="utf-8") as f:
    gossip_data = json.load(f)

# === Gossip Logic ===
gossip_texts = []
new_gossip_revealed = []
current_day = (datetime.date.today() - datetime.date(2025, 1, 1)).days + 1
available_gossip = filter_available_gossip(npc, gossip_data, current_day, nearby_npcs=scene_npcs[scene])
new_escape_clues = discover_escape_clues(npc, current_day)

for clue in new_escape_clues:
    st.info(f"🧭 Hinweis entdeckt: {clue}")

for g in gossip_data["gossips"]:
    if g["id"] in npc.get("known_gossip", []):
        gossip_texts.append(g["content"])

if npc["trust_level"] > 0.7:
    random.shuffle(available_gossip)
    for g in available_gossip[:2]:
        if g["id"] not in npc["known_gossip"]:
            npc["known_gossip"].append(g["id"])
            gossip_texts.append(g["content"])
            new_gossip_revealed.append(g["content"])

# === Background Image ===
if scene in scene_images and os.path.exists(scene_images[scene]):
    st.image(scene_images[scene], width=600)

# === NPC Info ===
st.header(f"👤 {npc['name']} ({npc['role']})")
col1, col2 = st.columns([1, 4])
if os.path.exists(npc_image):
    col1.image(npc_image, width=100)
col2.markdown(f"**Persönlichkeit:** {npc.get('personality')}")
col2.markdown(f"**Geschichte:** {npc.get('life_story')}")
col2.markdown(f"**Vertrauen:** {npc.get('trust_level', 0):.2f}")
col2.progress(npc.get("trust_level", 0.0))
if npc["trust_level"] > 0.8:
    col2.markdown("💖 Du bist ein enger Vertrauter.")
elif npc["trust_level"] > 0.6:
    col2.markdown("😊 Das Vertrauen wächst.")
elif npc["trust_level"] > 0.3:
    col2.markdown("🙂 Ein wenig Vertrauen ist da.")
else:
    col2.markdown("😐 Noch ziemlich distanziert.")
if npc.get("player_likes"):
    col2.markdown(f"**Mag:** {', '.join(npc['player_likes'])}")
if npc.get("player_dislikes"):
    col2.markdown(f"**Mag nicht:** {', '.join(npc['player_dislikes'])}")

npc_gossip_about = [
    g["content"] for g in gossip_data["gossips"]
    if g.get("target") == npc["name"] and g["id"] in npc.get("known_gossip", [])
]
if npc_gossip_about:
    st.markdown("### 🗨️ Was andere über sie sagen:")
    for line in npc_gossip_about:
        st.markdown(f"- {line}")

# === Player Input ===
user_input = st.text_input("Du:")
if user_input:
    update_player_preferences(npc, user_input)
    update_player_preferences_spacy(npc, user_input)
    npc["last_spoken"] = today_str

    suspicion_keywords = ["verschwinden", "opfer", "ritual", "tourist", "neujahr", "fliehen", "flucht", "geheimnis"]
    if any(word.lower() in user_input.lower() for word in suspicion_keywords):
        npc = increase_suspicion(npc, 0.15)

    for g in new_gossip_revealed:
        st.info(f"🗣️ Neues Gerücht: {g}")

    calendar_today = npc.get("calendar", {}).get(today_str, "")
    mood_today = npc.get("daily_mood", {}).get(today_str, "neutral")
    tone_hint = ""
    if npc.get("suspicion_level", 0.0) > 0.6:
        tone_hint = "Du hast ein ungutes Gefühl beim Spieler. Vielleicht verbirgst du etwas oder sprichst vorsichtiger."

    prompt = build_npc_prompt(
        npc, user_input, today, today_str, current_time_str,
        mood_today, calendar_today, gossip_texts,
        escape_clue_texts=npc.get("escape_clues", []), tone_hint=tone_hint
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        reply = re.sub(r"^\s*(\w+:)?", "", reply)

        translation = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": (
    "You are a professional German-to-English translator. Translate the following sentence "
    "into fluent, natural English. Do not explain or add commentary. Output only the English translation."
                )},
                {"role": "user", "content": reply}
            ],
            temperature=0.3
        ).choices[0].message.content.strip()

        st.markdown(f"**{npc['name']} 🇩🇪:** {reply}")
        st.markdown(f"🌍 **English:** {translation}")
        run_speech(reply, voice_name)
        st.audio("voice.mp3", format="audio/mp3")
        autoplay_audio("voice.mp3")

        log_conversation(npc, user_input, reply, today_str)
        npc["calendar"][today_str] = calendar_today
        npc["daily_mood"][today_str] = mood_today
        npc["new_year_mentioned"] = today_str
        npc["trust_level"] = round(min(npc["trust_level"] + 0.001, 1.0), 2)
        save_npc(npc, npc_file)
        share_gossip_with_others(npc, scene_npcs[scene], gossip_data)

    except Exception as e:
        import traceback
        st.error(f"⚠️ Fehler bei OpenRouter API:\n`{e}`")
        st.text(traceback.format_exc())

# === Summary Button ===
if st.button("🧾 Summarize all past conversations"):
    try:
        summary_de, summary_en = generate_summary(client, npc['name'], npc["conversation_log"])
        npc["conversation_summary"] = {
            "date": today_str,
            "summary_de": summary_de,
            "summary_en": summary_en
        }
        save_npc(npc, npc_file)

        st.success("✅ Zusammenfassung erstellt")
        st.markdown(f"📘 **Deutsch:** {summary_de}")
        run_speech(summary_de, voice_name, filename="summary_voice.mp3")
        st.audio("summary_voice.mp3", format="audio/mp3")
        autoplay_audio("summary_voice.mp3")
        st.markdown(f"🌍 **English:** {summary_en}")
    except Exception as e:
        st.error(f"⚠️ Fehler bei der Zusammenfassung: {e}")

# === Exit ===
if st.button("🔒 Close and Save"):
    try:
        npc_names = list_all_npcs()
        generate_summaries_for_today(client, npc_names, today_str)
        st.success("✅ Alle Gespräche von heute wurden gespeichert.")
        st.markdown("""
            <script>
                setTimeout(function() {
                    window.open('', '_self', '');
                    window.close();
                }, 1500);
            </script>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ Fehler beim Schließen: {e}")
