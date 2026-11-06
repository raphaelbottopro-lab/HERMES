"""Convertit le doc « Suivi PLF 2027 » (exporté en texte) en data/plf.json pour HERMÈS."""
import json, re, sys

src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")

def section(name):
    start = next(i for i, l in enumerate(lines) if l.strip() == f"## {name}")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start + 1:end]

def statut_of(etape):
    e = etape.lower()
    if "promulgu" in e: return "promulgue"
    if "définitivement" in e: return "definitif"
    if "adopté en séance" in e: return "adopte"
    if "adopté en commission" in e: return "commission"
    if "déposé" in e: return "depose"
    if "annoncé" in e: return "annonce"
    if "rejeté" in e or "retiré" in e: return "rejete"
    return "initial"

# Aujourd'hui
auj = [l for l in section("Aujourd'hui") if l.strip() and not l.startswith("Détail dans")]
titre_ligne = auj[0]
m = re.match(r"(.+?) – (.*)", titre_ligne)
aujourdhui = {
    "titre": m.group(1) if m else titre_ligne,
    "texte": m.group(2) if m else "",
    "points": [l[2:] for l in auj if l.startswith("- ")],
    "aVenir": next((l.split(":", 1)[1].strip() for l in auj if l.startswith("À venir")), ""),
}

# Tableau de suivi
tab = section("Tableau de suivi")
intro = next(l for l in tab if l.strip() and not l.startswith("|"))
rows = [l for l in tab if l.startswith("|")]
mesures = []
for r in rows[1:]:
    cells = [c.strip() for c in r.strip().strip("|").split(" | ")]
    if len(cells) < 5:
        continue
    mesure, initial, derniere, etape, date = cells[:5]
    texte = "PLFSS" if mesure.startswith("PLFSS") else "PLF"
    mesures.append({"mesure": mesure, "texte": texte, "initial": initial, "derniere": derniere,
                    "etape": etape, "date": date, "statut": statut_of(etape)})

# Journal
jour = section("Journal")
journal, cur = [], None
for l in jour:
    if l.startswith("### "):
        cur = {"titre": l[4:].strip(), "blocs": []}
        journal.append(cur)
    elif cur is not None and l.strip():
        if l.startswith("- "):
            cur["blocs"].append({"t": "li", "x": l[2:].strip()})
        else:
            cur["blocs"].append({"t": "p", "x": l.strip()})

MOIS = {m: i + 1 for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                                         "août", "septembre", "octobre", "novembre", "décembre"])}
for e in journal:
    mm = re.search(r"(\d{1,2}) (\w+) (\d{4})", e["titre"])
    e["date"] = f"{mm.group(3)}-{MOIS[mm.group(2)]:02d}-{int(mm.group(1)):02d}" if mm else ""
    # Un paragraphe court suivi de puces = titre d'entrée
    for i, b in enumerate(e["blocs"]):
        nxt = e["blocs"][i + 1] if i + 1 < len(e["blocs"]) else None
        if b["t"] == "p" and nxt and nxt["t"] == "li" and len(b["x"]) < 160 and not b["x"].startswith("Période"):
            b["t"] = "h"

# Calendrier
cal = [l for l in section("Calendrier") if l.strip()]
cal_intro = [l for l in cal if not l.startswith("- ")]
etapes = []
for l in cal:
    if l.startswith("- "):
        x = l[2:].strip()
        fait = "— fait" in x
        etapes.append({"texte": re.sub(r"\s—\s(fait|sans objet.*|interrompu)\.?$", "", x), "fait": fait,
                       "etat": "fait" if fait else ("sans objet" if "sans objet" in x else ("interrompu" if x.endswith("interrompu.") else "à venir"))})

# Statuts
statuts = []
for l in section("Mode d'emploi"):
    if l.startswith("|") and "Signification" not in l:
        c = [x.strip() for x in l.strip().strip("|").split(" | ")]
        if len(c) == 2:
            statuts.append({"statut": c[0], "sens": c[1]})

out = {
    "schema": 1,
    "maj": journal[0]["date"] if journal else "",
    "aujourdhui": aujourdhui,
    "intro": intro,
    "mesures": mesures,
    "journal": journal,
    "calendrier": {"intro": cal_intro[0] if cal_intro else "", "etapes": etapes,
                   "note": cal_intro[-1] if len(cal_intro) > 1 else ""},
    "statuts": statuts,
    # Champs courts affichés sur l'Accueil, tenus à jour par la tâche PLF
    "phase": "Rejeté en 1re lecture",
    "resumeCourt": "L’Assemblée a rejeté le volet recettes le 4 novembre, 458 voix contre et aucune pour. Le Sénat repart du texte du gouvernement : PLFSS dès le 9 novembre, PLF dès le 20.",
}
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(mesures)} mesures, {len(journal)} jours de journal, {len(etapes)} étapes, {len(statuts)} statuts")
