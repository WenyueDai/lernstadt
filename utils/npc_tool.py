import os
import json
import datetime

def load_npc(npc_name):
    path = f"role_json/{npc_name}.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            npc = json.load(f)
    else:
        npc = {}

    # Ensure critical fields exist
    npc["name"] = npc_name
    npc.setdefault("trust_level", 0.3)
    npc.setdefault("last_spoken", "")
    npc.setdefault("personality", "neutral")
    npc.setdefault("life_story", "Unbekannt.")
    npc.setdefault("role", "Einwohner")
    npc.setdefault("calendar", {})
    npc.setdefault("daily_mood", {})
    npc.setdefault("conversation_log", [])
    npc.setdefault("known_gossip", [])
    npc.setdefault("player_likes", [])
    npc.setdefault("player_dislikes", [])
    npc.setdefault("relationships", {})
    npc.setdefault("trust_levels", {})
    npc.setdefault("conversation_summary", {
        "date": "",
        "summary_de": "",
        "summary_en": ""
    })

    return npc, path

def save_npc(npc, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(npc, f, indent=2, ensure_ascii=False)

def update_trust(npc, today_str, last_spoken_str):
    today = datetime.date.fromisoformat(today_str)
    trust_change = 0.0

    if last_spoken_str:
        days_passed = (today - datetime.date.fromisoformat(last_spoken_str)).days
        if days_passed > 0:
            decay = 0.05 * days_passed
            npc["trust_level"] = max(npc["trust_level"] - decay, 0.0)
            trust_change -= decay
        elif days_passed < 0:
            npc["trust_level"] = min(npc["trust_level"] + 0.001, 1.0)
            trust_change += 0.001
    else:
        npc["trust_level"] = min(npc["trust_level"] + 0.001, 1.0)
        trust_change += 0.001

    npc["trust_level"] = round(npc["trust_level"], 2)
    npc["last_spoken"] = today_str
    return npc

def decay_trust(npc, today_str, last_spoken_str, days_threshold=3, decay_rate=0.05):
    if not last_spoken_str:
        return npc, None

    today = datetime.date.fromisoformat(today_str)
    last_spoken = datetime.date.fromisoformat(last_spoken_str)
    days_passed = (today - last_spoken).days

    if days_passed > days_threshold:
        decay = decay_rate * (days_passed - days_threshold)
        original = npc.get("trust_level", 0.05)
        npc["trust_level"] = max(0.0, original - decay)
        msg = f"Vertrauen sank um {decay:.2f} wegen {days_passed} Tagen ohne Gespräch."
        return npc, msg
    else:
        return npc, None

def log_conversation(npc, user_input, reply, today_str):
    npc["conversation_log"].append({
        "player": user_input,
        "npc": reply,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    npc["last_spoken"] = today_str
    npc.setdefault("conversation_summary", {
        "date": today_str,
        "summary_de": "",
        "summary_en": ""
    })

def list_all_npcs(npc_folder="role_json"):
    npc_files = []
    for filename in os.listdir(npc_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(npc_folder, filename)
            try:
                with open(filepath, encoding="utf-8") as f:
                    npc_data = json.load(f)
                    npc_files.append((npc_data, filepath))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return npc_files

def increase_suspicion(npc, amount=0.1):
    npc["suspicion_level"] = min(npc.get("suspicion_level", 0.0) + amount, 1.0)
    return npc

