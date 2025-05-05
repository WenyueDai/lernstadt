import os
import json

def share_gossip_with_others(npc, scene_npcs, gossip_data):
    """
    Shares known gossip from this NPC with other trusted NPCs in the same scene.

    Args:
        npc (dict): The NPC who just interacted with the player.
        scene_npcs (list): List of other NPC names in the same scene.
        gossip_data (dict): All available gossip from gossip_pool.json.
    """
    for other_name in scene_npcs:
        if other_name == npc["name"]:
            continue

        trust = npc.get("trust_levels", {}).get(other_name, 0)
        if trust > 0.6:
            other_file = f"role_json/{other_name.lower()}.json"
            if os.path.exists(other_file):
                with open(other_file, "r", encoding="utf-8") as f:
                    other_npc = json.load(f)

                other_npc.setdefault("known_gossip", [])
                new_gossips = 0

                for g_id in npc.get("known_gossip", []):
                    if g_id not in other_npc["known_gossip"]:
                        other_npc["known_gossip"].append(g_id)
                        new_gossips += 1

                if new_gossips > 0:
                    with open(other_file, "w", encoding="utf-8") as f:
                        json.dump(other_npc, f, indent=2, ensure_ascii=False)

def filter_available_gossip(npc, gossip_data, current_day, nearby_npcs=None):
    """Filters available gossip for the NPC based on known gossip and scene context.

    Args:
        npc (dict): The NPC whose gossip is being filtered.
        gossip_data (dict): All available gossip from gossip_pool.json.
        current_day (int): The current day in the game.
        nearby_npcs (list, optional): List of nearby NPCs. Defaults to None.

    Returns:
        list: A list of available gossip for the NPC.
    """
    known_ids = npc.get("known_gossip", [])
    npc_name = npc["name"]

    available = []
    for g in gossip_data["gossips"]:
        if g.get("day_unlocked", 1) > current_day:
            continue
        if g["id"] in known_ids:
            continue
        if npc_name not in g.get("exposed_to", []):
            continue

        if nearby_npcs:
            # Prioritize gossip targeting someone present
            if g.get("target") in nearby_npcs or g.get("target") is None:
                available.append(g)
        else:
            available.append(g)

    return available

