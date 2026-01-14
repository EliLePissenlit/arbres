import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

SRC1 = HERE / "data_raw" / "les-arbres.json"
SRC2 = HERE / "data_raw" / "arbres-remarquables-du-territoire-des-hauts-de-seine-hors-proprietes-privees.json"
OUT = HERE / "data" / "arbres.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

COMMON = {
    "nom_francais": ["nom_francais", "libellefrancais"],
    "hauteur": ["hauteurenm", "hauteur"],  
    "circonference": ["circonferenceencm", "circonference"], 
    "geo_point_2d": ["geo_point_2d"],
    "commune": ["commune", "arrondissement"],
    "code_insee": ["code_insee"],
    "nom_latin": ["nom_latin", "espece", "genre"],
}

def load(p: Path):
    with p.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    return obj if isinstance(obj, list) else obj.get("results", [])

def pick(d, keys):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None

def get_code_insee_paris(arrondissement):
    """Génère le code INSEE pour un arrondissement de Paris (75001 à 75020)"""
    if not arrondissement:
        return None
    val = str(arrondissement).strip().upper()
    if "BOIS DE BOULOGNE" in val:
        return "75016"
    if "BOIS DE VINCENNES" in val:
        return "75012"
    if "PARIS" in val and "ARRDT" in val:
        #  "1ER", "2E", "3E", etc.
        match = re.search(r'(\d+)(?:ER|E)?\s*ARRDT', val)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 20:
                return f"750{num:02d}"
    return None

def normalize_commune(val):
    """Normalise le nom de commune/arrondissement"""
    if not val:
        return None
    val = str(val).strip()
    val_upper = val.upper()
    # Bois de Boulogne et Bois de Vincennes
    if "BOIS DE BOULOGNE" in val_upper:
        return "Bois de Boulogne"
    if "BOIS DE VINCENNES" in val_upper:
        return "Bois de Vincennes"
    if "PARIS" in val_upper and "ARRDT" in val_upper:
        match = re.search(r'(\d+)(?:ER|E)?\s*ARRDT', val_upper)
        if match:
            num = int(match.group(1))
            if num == 1:
                return "Paris 1er"
            return f"Paris {num}ème"
        return "Paris"
    return val.title()

def normalize_nom_latin(rec):
    """Construit le nom latin à partir de nom_latin, ou genre + espece"""
    nom_latin = pick(rec, ["nom_latin"])
    if nom_latin:
        return nom_latin
    genre = pick(rec, ["genre"])
    espece = pick(rec, ["espece"])
    if genre and espece:
        return f"{genre} {espece}"
    return genre or espece or None

def normalize(rec, convert_m_to_cm=False, is_file1=False):
    result = {}
    for k, variants in COMMON.items():
        if k == "commune":
            val = pick(rec, variants)
            result[k] = normalize_commune(val)
        elif k == "nom_latin":
            result[k] = normalize_nom_latin(rec)
        elif k == "code_insee":
            if is_file1:
                arrondissement = pick(rec, ["arrondissement"])
                result[k] = get_code_insee_paris(arrondissement)
            else:
                val = pick(rec, variants)
                result[k] = val
        else:
            val = pick(rec, variants)
            if convert_m_to_cm and k in ["hauteur", "circonference"] and val is not None:
                if isinstance(val, (int, float)) and val < 1000:  
                    val = val * 100
            result[k] = val
    return result

data1 = [r for r in load(SRC1) if r.get("remarquable") == "OUI"]
data1_normalized = [normalize(r, convert_m_to_cm=True, is_file1=True) for r in data1]

# Fichier 2: 
data2 = load(SRC2)
data2_normalized = [normalize(r, convert_m_to_cm=True, is_file1=False) for r in data2]

data = data1_normalized + data2_normalized

with OUT.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK -> {OUT} ({len(data)} lignes)")