import datetime

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
    tone_hint=""
):
    escape_clue_texts = escape_clue_texts or []
    
    mbti = npc.get("mbti", "ENFP-T")

    mbti_traits = {
        "I": "introvertiert", "E": "extrovertiert",
        "N": "intuitiv", "S": "sinnesorientiert",
        "F": "gefühlsbetont", "T": "logisch",
        "J": "geplant", "P": "spontan",
        "A": "selbstsicher",  # Assertive
        "T": "emotional sensibel"  # Turbulent
    }
    
    core_type = mbti[:4]
    suffix = mbti[-1]  # A or T

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

    # New Year suspense logic
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

    # Suspicion logic
    suspicion_level = npc.get("suspicion_level", 0.0)
    suspicion_hint = ""
    if suspicion_level > 0.6:
        suspicion_hint = "Du hast ein ungutes Gefühl beim Spieler. Vielleicht verbirgst du etwas oder sprichst vorsichtiger."

    # Escape clues
    clues_text = "\n".join(f"- {clue}" for clue in escape_clue_texts)
    clue_block = f"\nMögliche Hinweise, die du kennst:\n{clues_text}" if clues_text else ""

    return f"""
Reply 'German speak please' if the user is not speaking German.

Du bist {npc['name']}, ein echter Bewohner von Lernstadt.
Heute ist {today.strftime('%A, %d %B %Y')}, und es ist {mood_today}.
Die aktuelle Uhrzeit ist {current_time_str} Uhr (Ortszeit).
Dein MBTI-Persönlichkeitstyp ist {mbti}.
Das bedeutet: {trait_expl} und {suffix_expl}.
Lass diesen Stil subtil in deinen Antworten durchscheinen.
Passe deine Ausdrucksweise an deine Persönlichkeit ({mbti}) an. Sei warm, distanziert oder verspielt – je nach Typ.


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
