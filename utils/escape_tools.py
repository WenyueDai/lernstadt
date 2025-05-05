import json
import os

def load_escape_clues(path="role_json/escape_clues.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["clues"]

def discover_escape_clues(npc, current_day):
    """Discovers new escape clues for the NPC based on the current day.

    Args:
        npc (dict): The NPC for whom escape clues are being discovered.
        current_day (int): The current day in the game.

    Returns:
        list: A list of new clues to display.
    """
    discovered = npc.setdefault("escape_clues", [])
    clues = load_escape_clues()

    new_clues = []
    for clue in clues:
        if clue["id"] in discovered:
            continue
        if npc["name"].lower() in [n.lower() for n in clue.get("found_by", [])] and clue["day_unlocked"] <= current_day:
            discovered.append(clue["id"])
            new_clues.append(clue["text"])
    return new_clues  # List of new clues to display
