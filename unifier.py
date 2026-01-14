import json
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

def normalize(rec, convert_m_to_cm=False):
    result = {}
    for k, variants in COMMON.items():
        val = pick(rec, variants)
        if convert_m_to_cm and k in ["hauteur", "circonference"] and val is not None:
            if isinstance(val, (int, float)) and val < 1000:  
                val = val * 100
        result[k] = val
    return result

data1 = [r for r in load(SRC1) if r.get("remarquable") == "OUI"]
data1_normalized = [normalize(r, convert_m_to_cm=True) for r in data1]

# Fichier 2: 
data2 = load(SRC2)
data2_normalized = [normalize(r, convert_m_to_cm=True) for r in data2]

data = data1_normalized + data2_normalized

with OUT.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK -> {OUT} ({len(data)} lignes)")