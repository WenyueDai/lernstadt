import re
import spacy

nlp = spacy.load("de_core_news_sm")

positive_words = ["liebe", "mag", "gern", "interessiere mich für", "toll", "cool", "like", "love", "fan", "super", "klasse", "mag sehr", "finde toll"]
negative_words = ["hasse", "mag nicht", "langweilig", "blöd", "schrecklich", "hate", "dislike", "finde schlecht", "finde blöd", "finde schrecklich", "nicht mögen", "nicht gut", "schlecht"]

def update_player_preferences(npc, text):
    for word in positive_words:
        if word in text.lower():
            topic = re.sub(rf".*{word}\\s+", "", text.lower()).strip(".!? ")
            if topic and topic not in npc["player_likes"]:
                npc["player_likes"].append(topic)
    for word in negative_words:
        if word in text.lower():
            topic = re.sub(rf".*{word}\\s+", "", text.lower()).strip(".!? ")
            if topic and topic not in npc["player_dislikes"]:
                npc["player_dislikes"].append(topic)

def update_player_preferences_spacy(npc, text):
    doc = nlp(text)
    like_verbs = {"lieben", "mag", "mögen", "liebe", "gern", "interessiere", "like", "love", "fan", "super", "klasse", "finde toll", "finde klasse", "finde super"}
    dislike_verbs = {"hasse", "nicht mögen", "mag nicht", "hasst", "dislike", "hassen", "finde schlecht", "finde blöd", "finde schrecklich"}
    for sent in doc.sents:
        for token in sent:
            if token.lemma_.lower() in like_verbs:
                for item in extract_objects(token):
                    if item not in npc["player_likes"]:
                        npc["player_likes"].append(item)
            elif token.lemma_.lower() in dislike_verbs or (
                token.lemma_ == "mögen" and any(child.text.lower() == "nicht" for child in token.children)
            ):
                for item in extract_objects(token):
                    if item not in npc["player_dislikes"]:
                        npc["player_dislikes"].append(item)

def extract_objects(verb_token):
    objects = []
    for child in verb_token.children:
        if child.dep_ in ("oa", "obj"):
            objects.append(child.text)
            for conj in child.conjuncts:
                objects.append(conj.text)
        elif child.dep_ == "prep" and child.text == "für":
            for obj in child.children:
                if obj.dep_ == "pobj":
                    objects.append(obj.text)
    return list(set(objects))
