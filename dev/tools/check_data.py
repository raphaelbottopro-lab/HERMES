"""Contrôle les données d'HERMÈS avant chaque publication.
Usage, depuis la racine du dépôt : python3 dev/tools/check_data.py
Code de sortie 0 = tout est bon ; 1 = au moins une ERREUR à corriger (les AVERTISSEMENTS n'empêchent pas de publier)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
ERR, WARN = [], []
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECTIONS = {"qui-a-dit-quoi", "politique", "economie", "social", "international", "regions"}
FORMATS = {"declaration", "developpe", "breve", "ligne", "region"}
CAMPS = {"Exécutif", "Institutions", "Extrême droite", "Droite", "Centre", "Gauche", "Autres", "Territoires", "International"}
STATUTS = {"annonce", "depose", "commission", "adopte", "rejete", "definitif", "promulgue", "initial"}
ETATS = {"fait", "à venir", "interrompu", "sans objet"}
INTERDITS = re.compile(r"cnews\.fr|europe1\.fr|pascal praud", re.I)

def err(m): ERR.append(m)
def warn(m): WARN.append(m)

def load(rel):
    p = DATA / rel
    if not p.exists():
        err(f"{rel} : fichier absent"); return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"{rel} : JSON invalide ({e})"); return None

def sources(where, lst, obligatoire=False):
    if lst is None:
        if obligatoire: err(f"{where} : sources manquantes")
        return
    if not isinstance(lst, list): err(f"{where} : 'sources' doit être une liste"); return
    for s in lst:
        if not isinstance(s, dict) or not s.get("nom"): err(f"{where} : source sans nom ({s})"); continue
        if s.get("url") and not str(s["url"]).startswith("http"): err(f"{where} : url invalide {s['url']}")

def textes(obj):
    if isinstance(obj, str): yield obj
    elif isinstance(obj, dict):
        for v in obj.values(): yield from textes(v)
    elif isinstance(obj, list):
        for v in obj: yield from textes(v)

index, fils, pers, glos, plf = load("index.json"), load("fils.json"), load("personnes.json"), load("glossaire.json"), load("plf.json")
load("chiffres.json"); sond = load("sondages.json")

fil_ids = set()
if fils:
    for f in fils.get("fils", []):
        w = f"fils.json [{f.get('id')}]"
        if not ID.match(str(f.get("id", ""))): err(f"{w} : id invalide")
        if f.get("id") in fil_ids: err(f"{w} : id en double")
        fil_ids.add(f.get("id"))
        for k in ("titre", "resume", "ouvert", "maj", "etat", "chrono"):
            if k not in f: err(f"{w} : champ '{k}' manquant")
        for k in ("ouvert", "maj"):
            if k in f and not ISO.match(str(f[k])): err(f"{w} : {k} doit être au format AAAA-MM-JJ")
        for c in f.get("chrono", []):
            if not ISO.match(str(c.get("date", ""))): err(f"{w} : date de chronologie invalide {c.get('date')}")
            if c.get("fin") and not ISO.match(str(c["fin"])): err(f"{w} : fin de chronologie invalide")
            sources(f"{w} chrono {c.get('date')}", c.get("sources"))

pers_ids = set()
if pers:
    for p in pers.get("personnes", []):
        w = f"personnes.json [{p.get('id')}]"
        if not ID.match(str(p.get("id", ""))): err(f"{w} : id invalide")
        if p.get("id") in pers_ids: err(f"{w} : id en double")
        pers_ids.add(p.get("id"))
        if p.get("camp") not in CAMPS: err(f"{w} : camp '{p.get('camp')}' hors liste {sorted(CAMPS)}")
        for k in ("nom", "fonction", "bio"):
            if not p.get(k): err(f"{w} : champ '{k}' manquant")
if fils:
    for f in fils.get("fils", []):
        for pid in f.get("personnes", []):
            if pid not in pers_ids: err(f"fils.json [{f['id']}] : personne inconnue '{pid}' (ajoute-la dans personnes.json)")

glos_ids = set()
if glos:
    for g in glos.get("entrees", []):
        if not ID.match(str(g.get("id", ""))): err(f"glossaire.json : id invalide {g.get('id')}")
        if g.get("id") in glos_ids: err(f"glossaire.json : id en double {g.get('id')}")
        glos_ids.add(g.get("id"))
        if not isinstance(g.get("texte"), list) or not g.get("texte"): err(f"glossaire.json [{g.get('id')}] : 'texte' doit être une liste de paragraphes")

def unites(ed):
    n = sum(1 for s in ed.get("sections", []) for it in s.get("items", []) if not it.get("vide"))
    return n + (1 if ed.get("debat") else 0) + (1 if ed.get("fait") else 0)

def check_edition(date):
    rel = f"editions/{date}.json"
    ed = load(rel)
    if not ed: return None
    w = rel
    if ed.get("date") != date: err(f"{w} : le champ date ({ed.get('date')}) ne correspond pas au nom du fichier")
    if ed.get("type") not in ("quotidien", "recap"): err(f"{w} : type doit être 'quotidien' ou 'recap'")
    for k in ("titre", "publieA", "essentiel", "sections", "agenda"):
        if k not in ed: err(f"{w} : champ '{k}' manquant")
    ids = set()
    for s in ed.get("sections", []):
        if s.get("id") not in SECTIONS: err(f"{w} : section '{s.get('id')}' hors liste {sorted(SECTIONS)}")
        for it in s.get("items", []):
            iw = f"{w} [{it.get('id')}]"
            if not ID.match(str(it.get("id", ""))): err(f"{iw} : id invalide")
            if it.get("id") in ids or it.get("id") in ("debat", "fait"): err(f"{iw} : id en double ou réservé")
            ids.add(it.get("id"))
            if it.get("format") not in FORMATS: err(f"{iw} : format '{it.get('format')}' hors liste {sorted(FORMATS)}")
            if not it.get("titre"): err(f"{iw} : titre manquant")
            if not isinstance(it.get("paragraphes"), list) or not it.get("paragraphes"): err(f"{iw} : 'paragraphes' doit être une liste non vide")
            if not isinstance(it.get("importance", 0), int) or not 0 <= it.get("importance", 0) <= 3: err(f"{iw} : importance entre 0 et 3")
            if it.get("format") == "declaration" and not (it.get("personne") or {}).get("nom"): err(f"{iw} : une déclaration a besoin de personne.nom")
            if it.get("format") == "region" and not it.get("lieu"): err(f"{iw} : une brève régionale a besoin de 'lieu'")
            sources(iw, it.get("sources"), obligatoire=not it.get("vide"))
            for fid in it.get("fils", []):
                if fid not in fil_ids: err(f"{iw} : fil inconnu '{fid}'")
            for pid in it.get("personnes", []) + ([it["personne"]["id"]] if (it.get("personne") or {}).get("id") else []):
                if pid not in pers_ids: warn(f"{iw} : personne '{pid}' absente de personnes.json")
            if it.get("lien") and it["lien"].get("onglet") not in ("plf", "plf-mesures", "plf-journal", "plf-calendrier", "fils", "sondages"):
                err(f"{iw} : lien.onglet inconnu")
    ess = ed.get("essentiel", [])
    if not 3 <= len(ess) <= 6: warn(f"{w} : l'essentiel compte {len(ess)} points (5 attendus)")
    for e in ess:
        if e.get("cible") and e["cible"] not in ids and e["cible"] not in ("debat", "fait"): err(f"{w} : essentiel → cible inconnue '{e['cible']}'")
    for fid in ed.get("filsMaj", []):
        if fid not in fil_ids: err(f"{w} : filsMaj → fil inconnu '{fid}'")
    cp = ed.get("comprendre")
    if isinstance(cp, str) and cp not in glos_ids: err(f"{w} : comprendre → notion '{cp}' absente de glossaire.json")
    for a in ed.get("agenda", []):
        if not ISO.match(str(a.get("date", ""))): err(f"{w} : date d'agenda invalide {a.get('date')}")
    if ed.get("debat"):
        d = ed["debat"]
        for k in ("question", "pour", "contre"):
            if not d.get(k): err(f"{w} : débat → '{k}' manquant")
    sd = ed.get("sondage")
    if sd:
        for k in ("institut", "publie", "resultats"):
            if not sd.get(k): err(f"{w} : sondage → '{k}' manquant")
        if not sd.get("echantillon") or not sd.get("marge"):
            if "non précis" not in str(sd.get("note", "")): warn(f"{w} : sondage sans échantillon ou marge : le préciser dans 'note'")
    for t in textes(ed):
        if INTERDITS.search(t): err(f"{w} : source ou nom exclu détecté ({INTERDITS.search(t).group(0)})")
    return ed

if index:
    eds = index.get("editions", [])
    dates = [e.get("date") for e in eds]
    if len(set(dates)) != len(dates): err("index.json : date d'édition en double")
    if index.get("derniere") not in dates: err("index.json : 'derniere' absente de la liste des éditions")
    if dates and index.get("derniere") != max(dates): err("index.json : 'derniere' n'est pas la date la plus récente")
    for e in eds:
        ed = check_edition(e.get("date"))
        if ed:
            if e.get("type") != ed.get("type"): err(f"index.json [{e.get('date')}] : type différent de l'édition")
            if e.get("sujets") != unites(ed): err(f"index.json [{e.get('date')}] : sujets = {e.get('sujets')}, attendu {unites(ed)}")
    pr = index.get("presidentielle", {})
    if not ISO.match(str(pr.get("tour1", ""))): err("index.json : presidentielle.tour1 manquant")
    known = set(dates)
    for f in (DATA / "editions").glob("*.json"):
        if f.stem not in known: warn(f"editions/{f.name} : fichier non listé dans index.json")

if sond:
    for v in sond.get("vagues", []):
        if not v.get("institut") or not ISO.match(str(v.get("publie", ""))) or not v.get("resultats"): err(f"sondages.json : vague incomplète ({v.get('institut')} {v.get('publie')})")

if plf:
    for k in ("maj", "phase", "resumeCourt", "aujourdhui", "intro", "mesures", "journal", "calendrier", "statuts"):
        if k not in plf: err(f"plf.json : champ '{k}' manquant")
    if plf.get("maj") and not ISO.match(plf["maj"]): err("plf.json : maj au format AAAA-MM-JJ")
    for i, m in enumerate(plf.get("mesures", [])):
        if m.get("statut") not in STATUTS: err(f"plf.json mesure {i} ({m.get('mesure')}) : statut '{m.get('statut')}' hors liste {sorted(STATUTS)}")
        if m.get("texte") not in ("PLF", "PLFSS"): err(f"plf.json mesure {i} : texte doit être 'PLF' ou 'PLFSS'")
        for k in ("mesure", "initial", "derniere", "etape", "date"):
            if not m.get(k): err(f"plf.json mesure {i} : '{k}' manquant")
    jd = [j.get("date") for j in plf.get("journal", [])]
    for j in plf.get("journal", []):
        if not ISO.match(str(j.get("date", ""))): err(f"plf.json journal : date invalide {j.get('date')}")
        for b in j.get("blocs", []):
            if b.get("t") not in ("p", "h", "li") or not b.get("x"): err(f"plf.json journal {j.get('date')} : bloc invalide {b}")
    if jd != sorted(jd, reverse=True): err("plf.json journal : les jours doivent aller du plus récent au plus ancien")
    if len(set(jd)) != len(jd): err("plf.json journal : jour en double")
    for e in plf.get("calendrier", {}).get("etapes", []):
        if e.get("etat") not in ETATS: err(f"plf.json calendrier : état '{e.get('etat')}' hors liste {sorted(ETATS)}")
    for t in textes(plf):
        if INTERDITS.search(t): err(f"plf.json : source exclue détectée ({INTERDITS.search(t).group(0)})")

for m in WARN: print("AVERTISSEMENT :", m)
for m in ERR: print("ERREUR :", m)
print(f"{len(ERR)} erreur(s), {len(WARN)} avertissement(s)")
sys.exit(1 if ERR else 0)
