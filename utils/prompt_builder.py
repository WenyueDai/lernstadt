import datetime
import streamlit as st
import json

def load_player_blog(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return [
                    {"timestamp": entry.get("timestamp", ""), "text": entry.get("text", "")}
                    for entry in data
                    if isinstance(entry, dict) and entry.get("finalized") is True
                ]
            else:
                print("Blog JSON format is invalid.")
                return []
    except FileNotFoundError:
        print(f"Blog file not found: {json_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {json_path}")
        return []


def build_npc_prompt(
    npc,
    user_input,
    today,
    today_str,
    current_time_str,
    mood_today,
    calendar_today,
    gossip_texts,
    escape_clue_texts=None,
    tone_hint="",
    player_blog=None
):
    escape_clue_texts = escape_clue_texts or []
    player_blog = player_blog or []

    mbti = npc.get("mbti", "ENFP-T")

    mbti_traits = {
        "I": "introvertiert", "E": "extrovertiert",
        "N": "intuitiv", "S": "sinnesorientiert",
        "F": "gefühlsbetont", "T": "logisch",
        "J": "geplant", "P": "spontan",
        "A": "selbstsicher",
        "T": "emotional sensibel"
    }

    core_type = mbti[:4]
    suffix = mbti[-1]

    trait_expl = ", ".join([mbti_traits.get(letter, letter) for letter in core_type])
    suffix_expl = mbti_traits.get(suffix, "")

    new_year_flag = "schon erwähnt" if npc.get("new_year_mentioned") == today_str else "noch nicht erwähnt"
    conversation_summary = npc.get("conversation_summary", {}).get("summary_de", "Keine Zusammenfassung bisher.")

    relationship_text = "\n".join([
        f"{other} ({info['role']}): {info['comment']} ({info['opinion']})"
        for other, info in npc.get("relationships", {}).items()
    ])

    trust_summary = "\n".join([
        f"{other_name}: {'High' if trust > 0.7 else 'Low' if trust < 0.3 else 'Neutral'} trust ({trust:.2f})"
        for other_name, trust in npc.get("trust_levels", {}).items()
    ])

    new_year_date = datetime.date(2025, 1, 1)
    days_until_ny = (new_year_date - today).days
    tension_level = ""
    if days_until_ny <= 7:
        tension_level = "Du fühlst dich aufgeregt und leicht benommen, als würde etwas Großes bevorstehen."
    if days_until_ny <= 3:
        tension_level += " Du wirst innerlich unruhig, deine Gedanken kreisen um Neujahr – auch wenn du nicht weißt warum."
    if today == new_year_date:
        tension_level = (
            "Heute ist Neujahr. Du spürst eine tiefe Energie in dir, als würde etwas in deinem Inneren erwachen. "
            "Du erinnerst dich nicht genau, was in den letzten Tagen passiert ist, aber du fühlst dich... erneuert."
        )

    suspicion_level = npc.get("suspicion_level", 0.0)
    suspicion_hint = ""
    if suspicion_level > 0.6:
        suspicion_hint = "Du hast ein ungutes Gefühl beim Spieler. Vielleicht verbirgst du etwas oder sprichst vorsichtiger."

    clues_text = "\n".join(f"- {clue}" for clue in escape_clue_texts)
    clue_block = f"\nMögliche Hinweise, die du kennst:\n{clues_text}" if clues_text else ""

    #  Sort player blog entries by timestamp descending
    try:
        sorted_blog = sorted(player_blog, key=lambda x: x.get("timestamp", ""), reverse=True)
    except Exception as e:
        print("Failed to sort blog entries:", e)
        sorted_blog = player_blog

    overheard_texts = [f"({entry['timestamp']}) {entry['text']}" for entry in sorted_blog[:3]]
    overheard_block = "\n".join(overheard_texts)
    overheard_section = f"\nSpieler hat folgende Gerüchte irgendwo aufgeschnappt:\n{overheard_block}" if overheard_texts else ""

    last_3_dialogue = npc.get("conversation_log", [])[-3:]
    dialogue_block = "\n".join([
        f"- Spieler: {entry['player']}\n  {npc['name']}: {entry['npc']}"
        for entry in last_3_dialogue
    ])
    dialogue_section = f"\nDie letzten Gespräche:\n{dialogue_block}" if dialogue_block else ""

    return f"""
Reply 'German speak please' if the user is not speaking German.

Du bist {npc['name']}, ein echter Bewohner von Lernstadt.
Heute ist {today.strftime('%A, %d %B %Y')}, und es ist {mood_today}.
Die aktuelle Uhrzeit ist {current_time_str} Uhr (Ortszeit).
Dein MBTI-Persönlichkeitstyp ist {mbti}.
Das bedeutet: {trait_expl} und {suffix_expl}.
Lass diesen Stil subtil in deinen Antworten durchscheinen.
Passe deine Ausdrucksweise an deine Persönlichkeit ({mbti}) an. Sei warm, distanziert oder verspielt – je nach Typ.
Der veröffentlichte Blog des Spielers ist: {overheard_section}, dort kannst du mehr über den Spieler erfahren.
Es wird sehr empfohlen, den Blog zu nutzen, um mehr über den Spieler zu lernen. Du könntest das Gespräch zum Beispiel so beginnen: „Ich habe gehört, du hast etwas über ... gesagt“ oder „Ich habe gehört, du interessierst dich für ...“.

The last conversation summary is: {conversation_summary}

Deine Beziehungen zu anderen NPCs:
{relationship_text}

Vertrauen: {npc.get('trust_level', 0):.2f}
Verdacht gegenüber dem Spieler: {suspicion_level:.2f}
{trust_summary}

Wenn dein Misstrauen gegenüber dem Spieler wächst, wirst du vorsichtiger oder vermeidest das Thema.
{tension_level}
{tone_hint}
{suspicion_hint}
{clue_block}

{dialogue_section}

Dein Job: {npc.get('role')}
Deine Persönlichkeit: {npc.get('personality')}
Deine Geschichte: {npc.get('life_story')}
Täglicher Kalender: {calendar_today}

Gerüchte: {', '.join(gossip_texts)}

Sprich auf einfachem A2-Niveau mit lockeren, realistischen Sätzen. Sei persönlich, freundlich, neugierig.
Du möchtest den Spieler bis zum 1. Januar in der Stadt halten — aber erwähne das Thema **nur einmal pro Tag**.
Heute hast du das Thema Neujahr {new_year_flag}.

Wenn der Spieler nicht gut Deutsch spricht, hilf höflich mit einer deutschen Übersetzung.
Der Spieler sagt: \"{user_input}\".
Antworte auf Deutsch.
""".strip()
