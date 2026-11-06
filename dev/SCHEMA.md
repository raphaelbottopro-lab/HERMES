# HERMÈS : format des données

L'appli (index.html) lit uniquement les fichiers JSON du dossier `data/`. Les tâches du matin écrivent ces fichiers, lancent `python3 dev/tools/check_data.py`, puis publient (commit + push sur `main`). GitHub Pages met l'appli à jour en une à deux minutes.

Règles communes :
- Dates au format `AAAA-MM-JJ`. Identifiants en minuscules ASCII avec tirets (`pol-budget`, `presidentielle-2027`).
- Textes en français, rédigés avec ses propres mots. Au plus une citation exacte de moins de 15 mots par source.
- Une source = `{"nom": "franceinfo", "url": "https://…"}`. Article payant : `"nom": "Le Monde (abonnés)"`.
- Jamais de lien ni de mention de CNews, d'Europe 1 ou de leurs animateurs et chroniqueurs : le contrôle bloque la publication.
- Modèle complet : `data/editions/2026-11-06.json`.

## data/index.json

```json
{"schema": 1, "maj": "2026-11-07T07:00:00+01:00", "derniere": "2026-11-07",
 "presidentielle": {"tour1": "2027-04-18", "tour2": "2027-05-02"},
 "editions": [{"date": "2026-11-07", "type": "quotidien", "titre": "Édition du samedi 7 novembre", "sujets": 18}, …]}
```
- `editions` : la plus récente en premier. `sujets` = nombre d'éléments des sections (hors `vide`) + 1 si `debat` + 1 si `fait` (le contrôle le recalcule).
- `maj` : heure de publication, avec le décalage horaire de Paris.

## data/editions/AAAA-MM-JJ.json

```json
{"schema": 1, "date": "2026-11-07", "type": "quotidien | recap",
 "titre": "Édition du samedi 7 novembre", "publieA": "07:00",
 "periode": "Depuis le vendredi 6 novembre, 7h.",
 "essentiel": [{"importance": 3, "texte": "…", "cible": "<id d'un élément>"}],
 "chiffres": {"cloture": "vendredi 6 novembre",
   "marches": [{"id": "cac40", "label": "CAC 40", "valeur": "8 205 pts", "variation": "+0,34 %", "sens": "hausse | baisse | neutre"}],
   "macro": [{"id": "inflation", "label": "Inflation octobre", "valeur": "3,4 %"}],
   "sources": [ … ]},
 "sondage": {"institut": "Ifop", "commanditaire": "LCI", "publie": "2026-11-03", "hypothese": "Hypothèse avec …",
   "echantillon": "1 012 personnes inscrites sur les listes électorales", "marge": "1,4 à 3,1 points",
   "note": "Écart avec la vague précédente du même institut.",
   "resultats": [{"nom": "Marine Le Pen", "parti": "RN", "valeur": 35, "evolution": "+1"}], "sources": [ … ]},
 "sections": [{"id": "qui-a-dit-quoi | politique | economie | social | international | regions", "titre": "…", "items": [ … ]}],
 "debat": {"question": "…", "pour": {"titre": "Ce que disent ses partisans (…)", "texte": "…"},
           "contre": {"titre": "Ce que répondent ses détracteurs", "texte": "…"}, "sources": [ … ]},
 "comprendre": "<id d'une entrée de glossaire.json>",
 "fait": {"texte": "…", "theme": "Économie", "sources": [ … ]},
 "agenda": [{"date": "2026-11-09", "fin": null, "libelle": "Lun. 9 nov.", "texte": "…"}],
 "filsMaj": ["<id de fil mis à jour aujourd'hui>"],
 "mention": "Édition rédigée à partir de sources officielles et de médias de sensibilités variées. Citations de moins de 15 mots, le reste reformulé."}
```

Titres des sections : « Qui a dit quoi ? », « Politique », « Économie », « Social et société », « International », « Régions », dans cet ordre. Le bloc `sondage` s'affiche sous « Ce que disent les Français » ; ne le remplir que pour un sondage publié récemment (sinon l'omettre). `chiffres.macro` : 4 indicateurs (inflation, PIB, chômage, taux de dépôt BCE), dernières valeurs publiées.

### Éléments (`items`)

Champs communs : `id`, `format`, `importance` (1 à 3), `titre`, `paragraphes` (liste), `sources`, et facultatifs `fils` (ids de fils), `personnes` (ids de personnes.json).

| format | usage | champs en plus |
|---|---|---|
| `declaration` | rubrique « Qui a dit quoi ? » | `personne`: {`id`, `nom`, `role`, `quand`}, `reactions` |
| `developpe` | 4 à 6 sujets développés par édition | `rubrique` (ex. « PRÉSIDENTIELLE 2027 »), `chiffresCles` [{`valeur`, `label`}], `pourquoi`, `reactions` [{`qui`, `texte`}], `patrimoine`, `note` |
| `breve` | une dizaine par édition | `rubrique`, `pourquoi`, `patrimoine`, `reactions` (facultatifs) |
| `ligne` | infos en 2-3 lignes (un seul paragraphe) | `etiquette` (ex. « PLF ») et `lien` {`onglet`: `plf`, `texte`: « Détail dans l'onglet PLF »} pour la ligne budget |
| `region` | section `regions` uniquement | `lieu` (« Bordeaux », « Nouvelle-Aquitaine », « Dordogne », « Périgueux », « Biarritz ») ; `"vide": true` pour « Rien de notable repéré depuis hier. » |

- `pourquoi` : une phrase « Pourquoi c'est important ». `patrimoine` : seulement quand c'est pertinent.
- `note` des sondages : institut, date, échantillon et marge d'erreur, ou « non précisés dans les sources consultées ».
- `essentiel[].cible` renvoie vers l'élément concerné (l'appli fait défiler jusqu'à lui).

### Le dimanche : récap de la semaine
`"type": "recap"`, `"titre": "Récap de la semaine du 2 au 8 novembre"`. Mêmes sections : les faits marquants du lundi au samedi par rubrique (surtout des `developpe` et `breve`), l'évolution des fils, les brèves des dernières 24 heures, et `agenda` = la semaine à venir.

## data/fils.json : sujets suivis dans la durée

```json
{"schema": 1, "fils": [{"id": "presidentielle-2027", "titre": "Présidentielle 2027", "ouvert": "2026-07-07", "maj": "2026-11-06",
  "resume": "Une ligne sur la dernière évolution (affichée dans les listes)",
  "etat": [{"titre": "Gauche", "texte": "Où on en est, mis à jour"}],
  "chrono": [{"date": "2026-11-04", "fin": null, "texte": "…", "sources": [ … ]}],
  "personnes": ["marine-le-pen"], "sondage": true, "plf": false, "region": null}]}
```
- Quand un fil bouge : mettre à jour `maj`, `resume` et `etat`, ajouter une entrée en tête de `chrono`, et ajouter son id dans `filsMaj` de l'édition.
- `sondage: true` : seulement pour la présidentielle (affiche le dernier sondage). `plf: true` : renvoie vers l'onglet PLF. `region` : nom du territoire pour un fil local.
- Créer un fil quand un sujet dure plusieurs jours ; ne jamais supprimer un fil existant.

## data/personnes.json : fiches « Qui est qui »

```json
{"schema": 1, "maj": "2026-11-06", "personnes": [{"id": "jordan-bardella", "nom": "Jordan Bardella", "fonction": "Président du RN",
  "camp": "Extrême droite", "parti": "RN", "bio": "Deux ou trois phrases factuelles et à jour."}]}
```
`camp` ∈ Exécutif, Institutions, Extrême droite, Droite, Centre, Gauche, Autres, Territoires, International. Ajouter chaque personne citée dans `personnes` d'un élément ; mettre à jour `fonction` et `bio` quand elles changent.

## data/glossaire.json : rubrique « Comprendre »

```json
{"schema": 1, "entrees": [{"id": "article-49-3", "titre": "Article 49.3", "texte": ["paragraphe", "…"], "theme": "Institutions | Économie | Marchés | Social | Europe", "ajoute": "2026-11-06"}]}
```
Chaque édition explique une notion : ajouter l'entrée si elle n'existe pas (ou compléter l'existante), puis mettre son id dans `comprendre`.

## data/chiffres.json et data/sondages.json : historiques

- `chiffres.json` : `{"series": {"cac40": [{"d": "2026-11-05", "v": 8205.37}], "oat10": […], "spread": […], "brent": […], "or": […], "eurusd": […]}}` : ajouter chaque jour la valeur de clôture (date de clôture, nombre décimal).
- `sondages.json` : `{"vagues": [ …même forme que edition.sondage… ]}` : ajouter chaque nouvelle vague d'intentions de vote présidentielle, la plus récente en premier.

## data/plf.json : onglet PLF (écrit par la tâche « Suivi PLF 2027 »)

```json
{"schema": 1, "maj": "2026-11-09", "phase": "Au Sénat",
 "resumeCourt": "Deux phrases affichées sur l'accueil.",
 "aujourdhui": {"titre": "lundi 9 novembre 2026", "texte": "Résumé du jour en une phrase.", "points": ["3 à 6 puces : article, changement, statut"], "aVenir": "Prochaines étapes."},
 "intro": "Au 9 novembre 2026, … (où en est le budget)",
 "mesures": [{"mesure": "Art. 6 – Assurance-vie", "texte": "PLF | PLFSS", "initial": "…", "derniere": "…", "etape": "Adopté en séance (Sénat)", "date": "12 novembre 2026", "statut": "annonce | depose | commission | adopte | rejete | definitif | promulgue | initial"}],
 "journal": [{"titre": "lundi 9 novembre 2026", "date": "2026-11-09", "blocs": [{"t": "p | h | li", "x": "…"}]}],
 "calendrier": {"intro": "…", "etapes": [{"texte": "20 novembre – Début de l'examen du PLF au Sénat", "fait": false, "etat": "fait | à venir | interrompu | sans objet"}], "note": "…"},
 "statuts": [{"statut": "Annoncé", "sens": "…"}]}
```
- `journal` : le jour le plus récent en premier ; ne jamais modifier ni supprimer les jours précédents.
- Blocs : `p` paragraphe, `h` titre d'une mesure (« Art. N – mesure : changement »), `li` puce. Les puces commencent par « Statut : », « Ce qui change : », « Concernés : », « Suite : » ou « Source : » (le libellé s'affiche en gras ; les adresses https:// deviennent des liens).
- `etape` d'une mesure : le texte (ex. « Adopté en commission (Sénat) ») ; `statut` : le code correspondant.
- `phase` : étiquette courte de l'état du budget (ex. « Au Sénat », « En CMP », « Adopté », « Promulgué »).
