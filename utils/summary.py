# summary.py
import os
import json

def generate_summary(client, npc_name, conv_log):
    full_conv = "\n".join([
        f"Spieler: {c['player']}\n{npc_name}: {c['npc']}" for c in conv_log[-10:]
    ])
    prompt = f"""
    Fasse dieses Gespräch mit {npc_name} in 3 Sätzen zusammen – fokussiere dich auf Stimmung, Vertrauen und ob Gerüchte gefallen sind.

    Gespräch:
    {full_conv}
    """
    summary_de = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    ).choices[0].message.content.strip()

    summary_en = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "Translate this German into natural English. No explanation."},
            {"role": "user", "content": summary_de}
        ],
        temperature=0.3
    ).choices[0].message.content.strip()

    return summary_de, summary_en

def generate_summaries_for_today(client, npc_list, today_str):
    for npc_name in npc_list:
        file_path = f"role_json/npcs/{npc_name}.json"
        if not os.path.exists(file_path):
            continue
        with open(file_path, encoding="utf-8") as f:
            npc = json.load(f)

        if npc.get("last_spoken") != today_str:
            continue

        if not npc.get("conversation_log"):
            continue

        summary_de, summary_en = generate_summary(client, npc_name, npc["conversation_log"])
        npc["conversation_summary"] = {
            "date": today_str,
            "summary_de": summary_de,
            "summary_en": summary_en
        }
        npc["conversation_log"] = []  # Clear log after summary

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(npc, f, indent=2, ensure_ascii=False)
