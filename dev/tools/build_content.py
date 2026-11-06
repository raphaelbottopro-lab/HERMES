"""Contenu de la première édition d'HERMÈS (6 novembre 2026) et des fichiers de référence.
Toutes les informations viennent des recherches du 6 novembre 2026 (sources citées dans chaque élément)."""
import json, os, sys

OUT = sys.argv[1]
os.makedirs(f"{OUT}/editions", exist_ok=True)

def dump(name, obj):
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)

S = {  # sources réutilisées
    "fi_regle": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/economie/budget/jordan-bardella-demande-le-vote-en-urgence-d-une-regle-d-or-dans-la-constitution-apres-le-rejet-du-budget-2027-a-l-assemblee-nationale_8269751.html"},
    "qz_regle": {"nom": "Quartz (AFP)", "url": "https://fr.qz.com/jordan-bardella-regle-or-constitution-budget-2027-110526"},
    "euronews_budget": {"nom": "Euronews", "url": "https://fr.euronews.com/2026/11/05/budget-2027-lassemblee-nationale-rejette-le-texte-a-lunanimite"},
    "fi_budget": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/economie/budget/l-assemblee-nationale-rejette-a-l-unanimite-le-budget-de-l-etat-2027-en-premiere-lecture_8268527.html"},
    "f24_budget": {"nom": "France 24", "url": "https://www.france24.com/fr/vid%C3%A9o/20261105-budget-2027-l-assembl%C3%A9e-nationale-rejette-%C3%A0-l-unanimit%C3%A9-le-projet-de-budget-de-l-%C3%A9tat"},
    "jdn_budget": {"nom": "Journal du Net", "url": "https://www.journaldunet.com/business/action-publique/1557631-les-deputes-rejettent-unanimement-le-projet-de-budget-2027/"},
    "fi_ruffin": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/replay-radio/les-informes-du-matin/les-informes-du-matin-du-vendredi-06-novembre-2026_8249929.html"},
    "qz_ifop": {"nom": "Quartz (AFP)", "url": "https://fr.qz.com/marine-pen-devance-melenchon-sondage-ifop-presidentielle-110426"},
    "jdd_ifop": {"nom": "Le JDD", "url": "https://www.lejdd.fr/politique/presidentielle-le-pen-domine-glucksmann-perd-du-terrain-lisnard-progresse-encore-les-enseignements-dun-nouveau-sondage-187734"},
    "yahoo_ifop": {"nom": "Yahoo Actualités", "url": "https://fr.news.yahoo.com/presidentielle-2027-duel-entre-jean-073944508.html"},
    "24m_livre": {"nom": "24matins", "url": "https://www.24matins.fr/soiree-du-livre-de-bardella-pourquoi-les-journalistes-sont-partis-1423661"},
    "yahoo_livre": {"nom": "Yahoo Actualités", "url": "https://fr.news.yahoo.com/mediapart-sest-vu-refuser-lacc%C3%A8s-073210551.html"},
    "bfm_cac": {"nom": "BFM Bourse", "url": "https://www.tradingsat.com/cac-40-FR0003500008/actualites/cac-40-la-debacle-des-valeurs-liees-a-l-ia-fait-chuter-le-nasdaq-de-4-le-cac-40-resiste-au-dessus-des-8200-points-1173263.html"},
    "spread": {"nom": "Banque de France via Idéal Investisseur", "url": "https://www.ideal-investisseur.fr/marches/spread-oat-bund.html"},
    "fe_spread": {"nom": "France Épargne", "url": "https://www.france-epargne.fr/news/lecart-entre-loat-et-le-bund-atteint-120-points-de-base-un-niveau-inedit-depuis-2012"},
    "abc_indus": {"nom": "ABC Bourse", "url": "https://www.abcbourse.com/marches/newsContent/705647"},
    "ymanci_bce": {"nom": "Ymanci", "url": "https://ymanci.fr/credit-immobilier/actualites/nouveaux-taux-bce-octobre-2026/"},
    "fi_lagarde": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/monde/europe/christine-lagarde-annonce-son-depart-anticipe-de-la-banque-centrale-europeenne-en-fevrier-2027_8258633.html"},
    "fi_lagarde2": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/politique/je-souhaite-avoir-la-liberte-de-m-engager-pourquoi-christine-lagarde-quitte-la-bce-a-six-mois-de-la-presidentielle_8260472.html"},
    "f24_greve": {"nom": "France 24", "url": "https://www.france24.com/fr/france/20261105-en-direct-grogne-sociale-monte-cran-greve-manifestations-interprofessionnelle-france-syndicat-police-lycee-fonctionnaires-retraites"},
    "ici_greve": {"nom": "ICI", "url": "https://www.ici.fr/infos/economie-social/direct-greve-du-5-novembre-les-syndicats-dans-la-rue-ce-jeudi-pour-les-salaires-et-contre-la-vie-chere-7257620"},
    "lessentiel_nunez": {"nom": "L’essentiel (AFP)", "url": "https://lessentiel.lu/fr/story/crises-en-france-le-5-novembre-nunez-veut-un-dispositif-robuste-103644650"},
    "titres_gj": {"nom": "France 24 via Titres Presse", "url": "https://www.titrespresse.com/28026062603/europe-info-jour"},
    "fi_midterms": {"nom": "franceinfo", "url": "https://www.franceinfo.fr/monde/usa/midterms-2018/resultats-midterms-2026-donald-trump-va-t-il-perdre-le-controle-du-senat-ou-de-la-chambre-des-representants-suivez-le-decompte-des-sieges-en-direct_8237248.html"},
    "libre_midterms": {"nom": "La Libre", "url": "https://dossiers.lalibre.be/midterms-2026/"},
    "rts_midterms": {"nom": "RTS", "url": "https://www.rts.ch/info/monde/2026/minute-par-minute/29402944.html"},
    "db_meloni": {"nom": "Daily Beirut", "url": "https://dailybeirut.com/fr/monde/negociations-ukraine-meloni-message-severe-conseil-europeen/"},
    "dem_meloni": {"nom": "Demócrata", "url": "https://www.democrata.es/fr/international/extension-l-italie-reclame-a-l-ue-de-designer-une-seule-voix-pour-les-negociations-de-paix-sur-l-ukraine/"},
    "eg_brent": {"nom": "L’EnerGeek", "url": "https://lenergeek.com/2026/11/06/petrole-rebond-brent-5-novembre-2026-ormuz/"},
    "trt_brent": {"nom": "TRT Français", "url": "https://www.trtfrancais.com/article/d2521cfe86ae"},
    "auto_brent": {"nom": "L’Automobiliste", "url": "https://lautomobiliste.fr/05/11/2026/petrole-baisse-prix-pompe-carburant-delai/"},
    "rue89_cm": {"nom": "Rue89 Bordeaux", "url": "https://rue89bordeaux.com/2026/11/echanges-de-lbd-au-conseil-municipal-de-bordeaux-sur-le-fiasco-securitaire-du-17-octobre/"},
    "gazette_cm": {"nom": "Bordeaux Gazette", "url": "https://www.bordeaux-gazette.com/17-octobre-a-bordeaux-echanges-tendus-au-conseil-municipal.html"},
    "ici_perigueux": {"nom": "ICI Périgord", "url": "https://www.ici.fr/nouvelle-aquitaine/dordogne-24/mobilisation-du-5-novembre-suivez-les-manifestations-en-dordogne-8224957"},
    "ici_biarritz": {"nom": "ICI Pays basque", "url": "https://www.ici.fr/nouvelle-aquitaine/pyrenees-atlantiques-64/biarritz"},
    "f3_biarritz": {"nom": "France 3 Nouvelle-Aquitaine", "url": "https://france3-regions.franceinfo.fr/nouvelle-aquitaine/pyrenees-atlantiques/biarritz"},
    "insee": {"nom": "Insee", "url": "https://www.insee.fr/fr/statistiques/2107840"},
    "conv_recession": {"nom": "The Conversation", "url": "https://theconversation.com/la-france-est-elle-entree-en-recession-en-2026-295759"},
    "an_ppl": {"nom": "Assemblée nationale, PPL n° 880", "url": "https://questions.assemblee-nationale.fr/dyn/17/textes/l17b0880_proposition-loi.pdf"},
    "ps_rn": {"nom": "Public Sénat", "url": "https://www.publicsenat.fr/actualites/politique/congres-du-rn-jordan-bardella-reelu-sans-suspens-president-du-rassemblement-national-remanie-les-instances-dirigeantes-du-parti"},
    "bn_bardella": {"nom": "Business News (AFP)", "url": "https://businessnews.com.tn/2026/10/24/france-bardella-reelu-a-9898-le-rassemblement-national-en-ordre-de-bataille-pour-lelysee/1424836/"},
    "ps_polony": {"nom": "Public Sénat", "url": "https://www.publicsenat.fr/actualites/politique/election-presidentielle-2027-qui-sont-les-candidats-declares-ou-presque"},
    "lcp_primaire": {"nom": "LCP", "url": "https://lcp.fr/actualites/primaire-socialiste-vainqueur-des-le-1er-tour-raphael-glucksmann-sera-le-candidat-de-la"},
    "i24_primaire": {"nom": "i24news", "url": "https://www.i24news.tv/fr/actu/france/artc-presidentielle-2027-raphael-glucksmann-vainqueur-de-la-primaire-de-la-gauche-des-le-premier-tour"},
    "f24_mediapart": {"nom": "France 24", "url": "https://www.france24.com/fr/tag/mediapart/"},
    "wiki_mediapart": {"nom": "Wikipédia, Mediapart", "url": "https://fr.wikipedia.org/wiki/Mediapart"},
    "slate_lepen": {"nom": "Slate", "url": "https://www.slate.fr/politique/condamnation-appel-marine-le-pen-jugement-sans-consequences-politiques-decision-citoyens-gagnante-sequence-justice-rn-bardella-election-presidentielle-2027"},
    "bluewin_lepen": {"nom": "blue News (AFP)", "url": "https://www.bluewin.ch/fr/infos/monde/marine-le-pen-peut-a-priori-tre-candidate-la-pr-sidentielle-li.3519786"},
    "lisnard_afp": {"nom": "Bourse Direct (AFP)", "url": "https://www.boursedirect.fr/fr/actualites/categorie/politique/presidentielle-david-lisnard-relance-l-idee-d-une-primaire-de-la-droite-et-du-centre-afp-72670b4b67234d51b334426e24f882ceb462d4f0"},
    "wiki_17oct": {"nom": "Wikipédia, Manifestations du 17 octobre 2026", "url": "https://fr.wikipedia.org/wiki/Manifestations_du_17_octobre_2026"},
    "hespress_17oct": {"nom": "Hespress (AFP)", "url": "https://fr.hespress.com/492970-macron-appelle-les-partis-a-condamner-les-violences-et-distingue-les-manifestants-des-casseurs.html"},
    "dh_17oct": {"nom": "La DH (AFP)", "url": "https://www.dhnet.be/dernieres-depeches/2026/10/19/crise-politique-et-violences-en-france-les-derniers-developpements-IJ6MWJT27VEWRB772VVKNHFOIM/"},
    "sud_bordeaux": {"nom": "Sud Radio", "url": "https://www.sudradio.fr/emission/a-la-une-de-sud-radio-101"},
    "wiki_nunez": {"nom": "Wikipédia, Laurent Nuñez", "url": "https://en.wikipedia.org/wiki/Laurent_Nu%C3%B1ez"},
    "iy_trappes": {"nom": "InfosYvelines", "url": "https://www.infosyvelines.fr/articles/trappes-hommage-national-preside-par-sebastien-lecornu"},
    "pm_trappes": {"nom": "Paris Match Belgique (AFP)", "url": "https://www.parismatch.be/actualites/monde/2026/10/30/attaque-raciste-a-trappes-le-suspect-avait-ete-interpelle-trois-jours-avant-les-faits-PV3ZAFJBCBAHVG2BCX6C7AD6FI/"},
    "wiki_truce": {"nom": "Wikipédia, trêve d’avril 2026", "url": "https://en.wikipedia.org/wiki/2026_Russo-Ukrainian_truce"},
    "lcp_budget": {"nom": "LCP", "url": "https://lcp.fr/dossiers/budget-2027-440523"},
    "cds_budget": {"nom": "Le Courrier des stratèges", "url": "https://www.lecourrierdesstrateges.fr/budget-2027-apres-le-rejet-que-va-t-il-se-passer-maintenant/"},
}

def src(*keys):
    return [S[k] for k in keys]

# ---------------------------------------------------------------- édition du jour
edition = {
    "schema": 1,
    "date": "2026-11-06",
    "type": "quotidien",
    "titre": "Édition du vendredi 6 novembre",
    "publieA": "07:00",
    "periode": "Depuis le jeudi 5 novembre, 7h. Première édition : quelques rappels des jours précédents.",
    "essentiel": [
        {"importance": 3, "texte": "Budget 2027 : l’Assemblée rejette le volet recettes à l’unanimité, le texte part au Sénat.", "cible": "pol-budget"},
        {"importance": 3, "texte": "Grève du 5 novembre : 575 000 manifestants selon l’Intérieur, 1,6 million selon la CGT.", "cible": "soc-greve"},
        {"importance": 3, "texte": "Midterms : les démocrates reprennent la Chambre et le Sénat, Trump dénonce des élections truquées.", "cible": "int-midterms"},
        {"importance": 2, "texte": "Sondage Ifop : Le Pen à 35-37 %, Mélenchon conforte sa 2e place, Glucksmann recule.", "cible": "pol-sondage"},
        {"importance": 2, "texte": "Bardella réclame une « règle d’or » budgétaire dans la Constitution.", "cible": "qdq-bardella"},
    ],
    "chiffres": {
        "cloture": "jeudi 5 novembre",
        "marches": [
            {"id": "cac40", "label": "CAC 40", "valeur": "8 205 pts", "variation": "+0,34 %", "sens": "hausse"},
            {"id": "oat10", "label": "OAT 10 ans", "valeur": "4,75 %", "variation": "Bund 3,27 %", "sens": "neutre"},
            {"id": "spread", "label": "Écart OAT-Bund", "valeur": "148 pb", "variation": "−8 pb sur la séance", "sens": "neutre"},
            {"id": "brent", "label": "Brent", "valeur": "98,3 $", "variation": "+3,67 $ après −9 % la veille", "sens": "hausse"},
            {"id": "or", "label": "Or", "valeur": "4 135 $", "variation": "+1,8 %", "sens": "hausse"},
            {"id": "eurusd", "label": "EUR/USD", "valeur": "1,123", "variation": "dollars pour 1 €", "sens": "neutre"},
        ],
        "macro": [
            {"id": "inflation", "label": "Inflation octobre", "valeur": "3,4 %"},
            {"id": "pib", "label": "PIB 3e trim.", "valeur": "−0,1 %"},
            {"id": "chomage", "label": "Chômage 2e trim.", "valeur": "8,3 %"},
            {"id": "bce", "label": "Taux de dépôt BCE", "valeur": "2,50 %"},
        ],
        "sources": src("bfm_cac", "spread", "eg_brent", "insee"),
    },
    "sondage": {
        "institut": "Ifop", "commanditaire": "LCI", "publie": "2026-11-03",
        "hypothese": "Hypothèse avec Philippe et Attal candidats",
        "echantillon": None, "marge": None,
        "note": "Écart avec la vague de mi-octobre. Échantillon et marge d’erreur non précisés dans les sources consultées.",
        "resultats": [
            {"nom": "Marine Le Pen", "parti": "RN", "valeur": 35, "evolution": "+1"},
            {"nom": "Jean-Luc Mélenchon", "parti": "LFI", "valeur": 18, "evolution": "+3"},
            {"nom": "Raphaël Glucksmann", "parti": "PS-PP", "valeur": 10, "evolution": "−2"},
            {"nom": "Édouard Philippe", "parti": "Horizons", "valeur": 9.5, "evolution": "−2,5"},
            {"nom": "David Lisnard", "parti": "droite", "valeur": 7, "evolution": "+1,5"},
            {"nom": "Gabriel Attal", "parti": "Renaissance", "valeur": 5, "evolution": "+1"},
        ],
        "sources": src("jdd_ifop", "qz_ifop"),
    },
    "sections": [
        {"id": "qui-a-dit-quoi", "titre": "Qui a dit quoi ?", "items": [
            {"id": "qdq-bardella", "format": "declaration", "importance": 2,
             "personne": {"id": "jordan-bardella", "nom": "Jordan Bardella", "role": "Président du RN", "quand": "jeudi 5 nov., vidéo sur ses réseaux"},
             "titre": "Bardella veut une « règle d’or » dans la Constitution",
             "paragraphes": ["Au lendemain du rejet du budget, il demande le vote rapide d’une « règle d’or » dans la Constitution : aucun budget ne pourrait être adopté s’il augmente l’endettement du pays. Il vise une adoption par le Parlement puis le Congrès en quelques semaines, et appelle les autres partis à le rejoindre."],
             "reactions": [
                 {"qui": "Bruno Retailleau (LR)", "texte": "veut aussi une règle d’or, mais par référendum avant la fin de l’année."},
                 {"qui": "Gauche et bloc central", "texte": "pas de réaction relevée à l’heure de l’édition."}],
             "sources": src("fi_regle", "qz_regle"), "fils": ["budget-2027"], "personnes": ["jordan-bardella", "bruno-retailleau"]},
            {"id": "qdq-amiel", "format": "declaration", "importance": 1,
             "personne": {"id": "david-amiel", "nom": "David Amiel", "role": "Ministre de l’Action et des Comptes publics", "quand": "mercredi 4 nov."},
             "titre": "Amiel met en garde contre l’effet présidentielle",
             "paragraphes": ["Après le vote des députés, il les invite à ne pas se laisser « hypnotiser par l’élection présidentielle » et rappelle qu’il ne reste que quelques semaines pour trouver un accord. À Matignon, on renvoie le compromis à l’après-Sénat."],
             "sources": src("euronews_budget"), "fils": ["budget-2027"], "personnes": ["david-amiel", "sebastien-lecornu"]},
            {"id": "qdq-ruffin", "format": "declaration", "importance": 1,
             "personne": {"id": "francois-ruffin", "nom": "François Ruffin", "role": "Debout !, candidat à la présidentielle", "quand": "ce matin sur franceinfo"},
             "titre": "Ruffin défend ses 40 chantiers",
             "paragraphes": ["Invité de la matinale, il a parlé salaires et mobilisations sociales, et défendu ses 40 chantiers pour « remettre la France debout »."],
             "sources": src("fi_ruffin"), "fils": ["presidentielle-2027"], "personnes": ["francois-ruffin"]},
        ]},
        {"id": "politique", "titre": "Politique", "items": [
            {"id": "pol-budget", "format": "ligne", "importance": 3, "etiquette": "PLF",
             "titre": "Budget 2027 : rejet unanime à l’Assemblée",
             "paragraphes": ["Budget 2027 : volet recettes rejeté par 458 voix contre et aucune pour. Le Sénat reprend le texte initial le 20 novembre."],
             "lien": {"onglet": "plf", "texte": "Détail dans l’onglet PLF"},
             "sources": src("fi_budget", "f24_budget"), "fils": ["budget-2027"]},
            {"id": "pol-sondage", "format": "developpe", "importance": 2, "rubrique": "PRÉSIDENTIELLE 2027",
             "titre": "Le Pen creuse l’écart, Glucksmann recule",
             "paragraphes": [
                 "Dans la vague Ifop pour LCI publiée le 3 novembre, Marine Le Pen (RN) recueille 35 à 37 % selon les hypothèses. Jean-Luc Mélenchon (LFI) monte à 17,5-18 % et devance ses poursuivants d’au moins deux points.",
                 "Raphaël Glucksmann (PS-Place publique) tombe à 10-13 %, contre 12-16 % mi-octobre. Édouard Philippe (Horizons) atteint 15 % s’il est le seul candidat du bloc central, 9,5 % si Gabriel Attal se présente aussi."],
             "pourquoi": "Trois semaines après sa primaire, Glucksmann perd du terrain dans la course à la qualification pour le second tour, que Mélenchon semble prendre en main à gauche.",
             "note": "Sondage Ifop pour LCI, publié le 3 nov. Échantillon et marge d’erreur non précisés dans les sources consultées.",
             "sources": src("qz_ifop", "jdd_ifop", "yahoo_ifop"), "fils": ["presidentielle-2027"],
             "personnes": ["marine-le-pen", "jean-luc-melenchon", "raphael-glucksmann", "edouard-philippe", "gabriel-attal"]},
            {"id": "pol-mediapart", "format": "breve", "importance": 1, "rubrique": "MÉDIAS",
             "titre": "Livre de Bardella : Mediapart refoulé, la presse quitte la soirée",
             "paragraphes": ["Mercredi soir à Paris, un reporter de Mediapart s’est vu refuser l’entrée malgré son billet. Presque tous les journalistes accrédités sont alors partis. Le journal et le président du RN s’opposent depuis fin septembre sur des messages antisémites que Mediapart lui attribue et qu’il conteste."],
             "sources": src("24m_livre", "yahoo_livre"), "fils": ["bardella-mediapart", "presidentielle-2027"], "personnes": ["jordan-bardella"]},
        ]},
        {"id": "economie", "titre": "Économie", "items": [
            {"id": "eco-marches", "format": "breve", "importance": 2, "rubrique": "MARCHÉS",
             "titre": "Le CAC 40 tient malgré la chute de l’IA à Wall Street",
             "paragraphes": ["L’indice parisien gagne 0,34 % à 8 205 points jeudi, alors que le Nasdaq perd 4 % sur des craintes d’une réglementation plus stricte de l’intelligence artificielle aux États-Unis. L’écart de taux entre la France et l’Allemagne se resserre à 148 points de base."],
             "patrimoine": "Les banques tiennent compte de l’OAT 10 ans dans leurs barèmes de crédit immobilier : tant que l’écart avec l’Allemagne reste proche de 150 points, les taux proposés aux emprunteurs restent sous pression.",
             "sources": src("bfm_cac", "spread", "fe_spread")},
            {"id": "eco-industrie", "format": "ligne", "importance": 1,
             "titre": "Production industrielle en baisse",
             "paragraphes": ["Industrie : la production industrielle recule de 0,5 % en septembre."],
             "sources": src("abc_indus")},
            {"id": "eco-bce", "format": "ligne", "importance": 1,
             "titre": "BCE : taux inchangés, départ de Lagarde en février",
             "paragraphes": ["BCE : taux de dépôt maintenu à 2,50 % le 29 octobre, prochaine décision le 17 décembre. Christine Lagarde quittera la présidence le 7 février 2027."],
             "sources": src("ymanci_bce", "fi_lagarde"), "personnes": ["christine-lagarde"]},
        ]},
        {"id": "social", "titre": "Social et société", "items": [
            {"id": "soc-greve", "format": "developpe", "importance": 3, "rubrique": "MOUVEMENTS SOCIAUX",
             "titre": "Grève du 5 novembre : une mobilisation massive pour les salaires",
             "chiffresCles": [{"valeur": "575 000", "label": "selon l’Intérieur"}, {"valeur": "1,6 million", "label": "selon la CGT"}],
             "paragraphes": [
                 "À l’appel des syndicats, salariés du public et du privé, retraités, lycéens et étudiants ont défilé pour les salaires et les services publics, dans 180 cortèges selon le ministère, dont 350 000 personnes à Paris selon la CGT.",
                 "Des heurts ont éclaté en tête de cortège à Lyon, où la préfecture compte 30 500 manifestants et la CGT 55 000. Un photographe de l’AFP a été frappé à coups de matraque par des CRS. 70 000 policiers et gendarmes étaient mobilisés."],
             "pourquoi": "La journée prolonge la colère sociale de l’automne, après le 17 octobre marqué par des violences et des pillages dans plusieurs villes. Des gilets jaunes appellent à de nouvelles actions ce vendredi et samedi.",
             "sources": src("f24_greve", "ici_greve", "lessentiel_nunez", "titres_gj"), "fils": ["mobilisation-automne-2026"], "personnes": ["laurent-nunez"]},
        ]},
        {"id": "international", "titre": "International", "items": [
            {"id": "int-midterms", "format": "breve", "importance": 3, "rubrique": "ÉTATS-UNIS",
             "titre": "Les démocrates reprennent le Congrès",
             "paragraphes": ["Après les élections de mi-mandat du 3 novembre, ils détiennent la majorité à la Chambre des représentants et au Sénat, avec 54 sièges sur 100 d’après les derniers décomptes. Donald Trump dénonce des élections « truquées »."],
             "sources": src("fi_midterms", "libre_midterms", "rts_midterms"), "fils": ["guerre-iran-petrole"], "personnes": ["donald-trump"]},
            {"id": "int-ukraine", "format": "breve", "importance": 2, "rubrique": "UKRAINE",
             "titre": "Meloni réclame une voix unique pour l’Europe",
             "paragraphes": ["Dans une lettre à António Costa, président du Conseil européen, la Première ministre italienne critique la dispersion des Vingt-Sept, avant les pourparlers Ukraine–Russie prévus le 11 novembre à Abou Dhabi sous médiation américaine."],
             "sources": src("db_meloni", "dem_meloni"), "fils": ["ukraine-paix"], "personnes": ["giorgia-meloni", "antonio-costa"]},
            {"id": "int-petrole", "format": "ligne", "importance": 2,
             "titre": "Pétrole : le Brent sous 100 $, puis rebond",
             "paragraphes": ["Pétrole : le Brent est passé sous 100 $ mercredi, sur l’espoir d’une désescalade dans la guerre entre les États-Unis et l’Iran, puis a rebondi jeudi à 98,3 $ après de nouveaux incidents visant des navires."],
             "sources": src("eg_brent", "trt_brent"), "fils": ["guerre-iran-petrole"]},
        ]},
        {"id": "regions", "titre": "Régions", "items": [
            {"id": "reg-bordeaux", "format": "region", "importance": 2, "lieu": "Bordeaux",
             "titre": "Bordeaux chiffre les dégâts du 17 octobre",
             "paragraphes": ["Au conseil municipal du 2 novembre, Thomas Cazenave chiffre à 350 000 € les dégâts du 17 octobre pour la ville et la métropole, et à 8-10 M€ ceux des 81 commerces touchés. Il demande que les cortèges évitent l’hypercentre ; l’opposition le renvoie à ses promesses sur la sécurité."],
             "sources": src("rue89_cm", "gazette_cm"), "fils": ["bordeaux-17-octobre"], "personnes": ["thomas-cazenave"]},
            {"id": "reg-perigueux", "format": "region", "importance": 1, "lieu": "Périgueux",
             "titre": "Périgueux : 2 400 à 3 500 manifestants",
             "paragraphes": ["Entre 2 400 manifestants selon la préfecture et 3 500 selon la CGT ont défilé jeudi."],
             "sources": src("ici_perigueux"), "fils": ["mobilisation-automne-2026"]},
            {"id": "reg-biarritz", "format": "region", "importance": 1, "lieu": "Biarritz",
             "titre": "Biarritz : le banquet du Canon français fait débat",
             "paragraphes": ["Banquet du Canon français le 28 novembre : la préfecture réclame 45 000 € aux organisateurs pour la sécurité, et cent personnalités appellent à une chaîne humaine."],
             "sources": src("ici_biarritz", "f3_biarritz"), "fils": ["biarritz-canon-francais"]},
            {"id": "reg-na", "format": "region", "importance": 0, "lieu": "Nouvelle-Aquitaine · Dordogne",
             "titre": "Rien de notable", "vide": True,
             "paragraphes": ["Rien de notable repéré depuis hier."], "sources": []},
        ]},
    ],
    "debat": {
        "id": "debat-regle-or",
        "question": "Faut-il inscrire une « règle d’or » budgétaire dans la Constitution ?",
        "pour": {"titre": "Ce que disent ses partisans (RN, LR)", "texte": "Elle obligerait chaque gouvernement à cesser d’alourdir la dette, alors que la France n’a plus voté de budget à l’équilibre depuis 1974, et rassurerait les prêteurs au moment où l’écart de taux avec l’Allemagne frôle 150 points."},
        "contre": {"titre": "Ce que répondent ses détracteurs", "texte": "Une règle rigide priverait l’État de marge en cas de crise ou de récession, et la France dispose déjà d’un cadre : la loi organique de 2012 sur les finances publiques et les règles budgétaires européennes."},
        "sources": src("fi_regle", "an_ppl", "spread"),
    },
    "comprendre": "rejet-budget",
    "fait": {"texte": "Une récession technique, c’est deux trimestres de baisse du PIB d’affilée. La France a fait −0,2 % au 1er trimestre, 0,0 % au 2e puis −0,1 % au 3e : pas de récession technique, mais neuf mois sans croissance.",
             "theme": "Économie", "sources": src("conv_recession", "insee")},
    "agenda": [
        {"date": "2026-11-06", "fin": "2026-11-07", "libelle": "6-7 nov.", "texte": "Actions « six-seven populaire » appelées par des gilets jaunes"},
        {"date": "2026-11-09", "libelle": "Lun. 9 nov.", "texte": "Le Sénat commence l’examen du PLFSS 2027"},
        {"date": "2026-11-11", "libelle": "Mer. 11 nov.", "texte": "Pourparlers Ukraine–Russie à Abou Dhabi, sous médiation américaine"},
        {"date": "2026-11-13", "libelle": "Ven. 13 nov.", "texte": "Insee : inflation définitive d’octobre"},
        {"date": "2026-11-20", "libelle": "Ven. 20 nov.", "texte": "Le Sénat commence l’examen du PLF 2027"},
        {"date": "2026-11-28", "libelle": "Sam. 28 nov.", "texte": "Banquet du Canon français à Biarritz, contre-rassemblement annoncé"},
    ],
    "filsMaj": ["presidentielle-2027", "budget-2027", "mobilisation-automne-2026", "guerre-iran-petrole"],
    "mention": "Édition rédigée à partir de sources officielles et de médias de sensibilités variées. Citations de moins de 15 mots, le reste reformulé.",
}
nb_sujets = sum(len([i for i in s["items"] if not i.get("vide")]) for s in edition["sections"]) + 2  # + débat et fait
edition["sujets"] = nb_sujets
dump("editions/2026-11-06.json", edition)

# ---------------------------------------------------------------- fils
fils = {"schema": 1, "fils": [
    {"id": "presidentielle-2027", "titre": "Présidentielle 2027", "ouvert": "2026-07-07", "maj": "2026-11-06",
     "resume": "Sondage Ifop : Glucksmann recule", "sondage": True,
     "etat": [
         {"titre": "Calendrier", "texte": "1er tour le dimanche 18 avril 2027, second tour le 2 mai."},
         {"titre": "Rassemblement national", "texte": "Marine Le Pen est candidate : en appel, son inéligibilité ferme a été ramenée à 15 mois. Son congrès d’Orléans a lancé la campagne fin octobre et réélu Jordan Bardella à la tête du parti."},
         {"titre": "Gauche", "texte": "Raphaël Glucksmann porte le PS, Place publique et la GRS après sa primaire. Jean-Luc Mélenchon (LFI) et François Ruffin (Debout !) font campagne de leur côté ; Marine Tondelier et Fabien Roussel sont testés dans les sondages."},
         {"titre": "Centre et droite", "texte": "Pas de primaire à ce stade. Édouard Philippe (Horizons), Bruno Retailleau (LR) et David Lisnard sont candidats, Gabriel Attal (Renaissance) est testé. Lisnard réclame une primaire ouverte."},
         {"titre": "Autres", "texte": "Éric Zemmour (Reconquête), Nicolas Dupont-Aignan et Natacha Polony sont aussi dans la course."}],
     "chrono": [
         {"date": "2026-11-04", "texte": "Lancement du livre de Jordan Bardella : un reporter de Mediapart est refoulé, presque tous les journalistes quittent la soirée.", "sources": src("24m_livre")},
         {"date": "2026-11-03", "texte": "Sondage Ifop pour LCI : Le Pen à 35-37 %, Mélenchon à 17,5-18 %, Glucksmann recule à 10-13 %.", "sources": src("qz_ifop", "jdd_ifop")},
         {"date": "2026-10-29", "texte": "Christine Lagarde quittera la BCE le 7 février 2027 pour retrouver « la liberté de m’engager », ce qui relance les spéculations sur une candidature.", "sources": src("fi_lagarde2")},
         {"date": "2026-10-24", "texte": "Congrès du RN à Orléans : Jordan Bardella réélu président avec 98,98 % des voix, Marine Le Pen ouvre sa campagne.", "sources": src("bn_bardella", "ps_rn")},
         {"date": "2026-10-14", "texte": "Natacha Polony se déclare candidate sur France Inter.", "sources": src("ps_polony")},
         {"date": "2026-10-11", "texte": "Raphaël Glucksmann remporte la primaire socialiste dès le 1er tour, avec 66,17 % des voix.", "sources": src("lcp_primaire", "i24_primaire")},
         {"date": "2026-09-28", "fin": "2026-10-09", "texte": "Mediapart publie des messages antisémites qu’il attribue à Jordan Bardella, puis ses éléments d’authentification. Bardella dénonce des faux et annonce des poursuites.", "sources": src("f24_mediapart", "wiki_mediapart")},
         {"date": "2026-07-07", "texte": "La cour d’appel de Paris condamne Marine Le Pen mais réduit son inéligibilité ferme : sa candidature redevient juridiquement possible.", "sources": src("slate_lepen", "bluewin_lepen")}],
     "personnes": ["marine-le-pen", "jordan-bardella", "jean-luc-melenchon", "raphael-glucksmann", "edouard-philippe", "gabriel-attal", "bruno-retailleau", "david-lisnard", "francois-ruffin", "christine-lagarde"]},
    {"id": "budget-2027", "titre": "Budget 2027", "ouvert": "2026-10-01", "maj": "2026-11-06", "plf": True,
     "resume": "Rejet unanime à l’Assemblée",
     "etat": [
         {"titre": "Où en est le texte", "texte": "L’Assemblée a rejeté le volet recettes du PLF le 4 novembre, par 458 voix contre et aucune pour : le Sénat repart du texte du gouvernement, qui vise un déficit de 5 % du PIB en 2027. Le PLFSS avait été rejeté le 23 octobre."},
         {"titre": "Calendrier", "texte": "PLFSS au Sénat du 9 au 18 novembre ; PLF du 20 novembre au 9 décembre. Au-delà de 70 jours d’examen, soit le 17 décembre, le budget peut passer par ordonnance."},
         {"titre": "Les options du gouvernement", "texte": "Matignon renvoie le compromis à l’après-Sénat. La presse évoque un 49.3 en lecture ultérieure, que Sébastien Lecornu avait écarté le 17 septembre."}],
     "chrono": [
         {"date": "2026-11-05", "texte": "Jordan Bardella demande une « règle d’or » budgétaire dans la Constitution ; Bruno Retailleau propose un référendum.", "sources": src("fi_regle")},
         {"date": "2026-11-04", "texte": "L’Assemblée rejette la première partie du PLF à l’unanimité (458 contre, 0 pour) ; le texte initial part au Sénat.", "sources": src("fi_budget", "jdn_budget")},
         {"date": "2026-10-23", "texte": "Le PLFSS est rejeté en première lecture à l’Assemblée.", "sources": src("fi_budget")},
         {"date": "2026-10-13", "texte": "Ouverture de la séance publique sur la première partie du PLF, après son rejet en commission des finances le 9 octobre.", "sources": src("lcp_budget")},
         {"date": "2026-10-01", "texte": "Dépôt du PLF et du PLFSS 2027 à l’Assemblée.", "sources": src("lcp_budget")}],
     "personnes": ["sebastien-lecornu", "david-amiel", "philippe-juvin", "christine-lavarde", "jordan-bardella", "bruno-retailleau"]},
    {"id": "mobilisation-automne-2026", "titre": "Mobilisation sociale d’automne", "ouvert": "2026-10-17", "maj": "2026-11-06",
     "resume": "Grève interprofessionnelle du 5 novembre",
     "etat": [
         {"titre": "Les revendications", "texte": "Vie chère, salaires et services publics. Le mouvement réunit syndicats, gilets jaunes, lycéens et étudiants, qui réclament notamment 10 milliards d’euros pour l’éducation."},
         {"titre": "Les temps forts", "texte": "Le 17 octobre, 550 000 à 800 000 manifestants selon les sources, et des pillages dans plusieurs grandes villes. Le 5 novembre, la grève interprofessionnelle a réuni 575 000 personnes selon l’Intérieur, 1,6 million selon la CGT."},
         {"titre": "La réponse de l’État", "texte": "Emmanuel Macron a condamné les violences le 18 octobre et refusé la démission de Laurent Nuñez. Sébastien Lecornu a reçu les syndicats. 70 000 policiers et gendarmes étaient mobilisés le 5 novembre."}],
     "chrono": [
         {"date": "2026-11-06", "fin": "2026-11-07", "texte": "Des gilets jaunes appellent à de nouvelles actions, baptisées « six-seven populaire ».", "sources": src("titres_gj")},
         {"date": "2026-11-05", "texte": "Grève interprofessionnelle : 575 000 manifestants selon l’Intérieur, 1,6 million selon la CGT ; heurts à Lyon.", "sources": src("f24_greve", "ici_greve")},
         {"date": "2026-11-03", "texte": "Nouveaux blocages de lycées et d’universités à l’appel des organisations de jeunesse.", "sources": src("lessentiel_nunez")},
         {"date": "2026-10-19", "texte": "Les syndicats sont conviés à Matignon ; Emmanuel Macron refuse la démission de Laurent Nuñez.", "sources": src("dh_17oct", "wiki_nunez")},
         {"date": "2026-10-18", "texte": "Allocution d’Emmanuel Macron, qui condamne les violences et distingue manifestants et casseurs.", "sources": src("hespress_17oct")},
         {"date": "2026-10-17", "texte": "Journée contre la vie chère : 550 000 manifestants selon l’Intérieur, pillages et violences dans plusieurs villes, 1 800 interpellations.", "sources": src("hespress_17oct", "wiki_17oct")}],
     "personnes": ["emmanuel-macron", "sebastien-lecornu", "laurent-nunez"]},
    {"id": "guerre-iran-petrole", "titre": "Guerre États-Unis – Iran et pétrole", "ouvert": "2026-02-01", "maj": "2026-11-06",
     "resume": "Le Brent repasse sous 100 $, puis rebondit",
     "etat": [
         {"titre": "Le contexte", "texte": "Depuis février 2026, la guerre entre les États-Unis et l’Iran perturbe le détroit d’Ormuz, par où transite environ 20 % du pétrole mondial. Le Brent était au-dessus de 100 $ depuis début octobre."},
         {"titre": "Les effets en Europe", "texte": "Le choc énergétique a relancé l’inflation (3,4 % en France en octobre) et poussé la BCE à relever ses taux deux fois en 2026, jusqu’à 2,50 %."},
         {"titre": "Depuis les midterms", "texte": "La victoire démocrate au Congrès nourrit l’espoir d’une désescalade : le Brent a perdu près de 9 % le 4 novembre avant de rebondir le lendemain."}],
     "chrono": [
         {"date": "2026-11-05", "texte": "Le Brent rebondit à 98,3 $ après de nouveaux incidents visant des navires.", "sources": src("eg_brent")},
         {"date": "2026-11-04", "texte": "Le Brent chute de près de 9 % et repasse sous 100 $ ; l’AIE remet des stocks sur le marché.", "sources": src("trt_brent", "auto_brent")},
         {"date": "2026-11-03", "texte": "Élections de mi-mandat : les démocrates reprennent le Congrès.", "sources": src("fi_midterms")},
         {"date": "2026-10-29", "texte": "La BCE maintient son taux de dépôt à 2,50 %.", "sources": src("ymanci_bce")},
         {"date": "2026-09-10", "texte": "Deuxième hausse de taux de la BCE en 2026, à 2,50 %.", "sources": src("ymanci_bce")}],
     "personnes": ["donald-trump", "christine-lagarde"]},
    {"id": "ukraine-paix", "titre": "Ukraine : négociations de paix", "ouvert": "2026-04-11", "maj": "2026-11-06",
     "resume": "Meloni réclame une voix unique pour l’UE",
     "etat": [
         {"titre": "Où en sont les discussions", "texte": "Les États-Unis mènent la médiation entre l’Ukraine et la Russie. Une nouvelle session est prévue le 11 novembre à Abou Dhabi."},
         {"titre": "La place de l’Europe", "texte": "Les Vingt-Sept peinent à parler d’une seule voix ; Giorgia Meloni demande un représentant unique doté d’un mandat clair."}],
     "chrono": [
         {"date": "2026-11-05", "texte": "Lettre de Giorgia Meloni à António Costa pour réclamer une voix unique de l’UE.", "sources": src("db_meloni", "dem_meloni")},
         {"date": "2026-04-11", "fin": "2026-04-13", "texte": "Trêve de Pâques orthodoxe de 32 heures, émaillée d’accusations de violations.", "sources": src("wiki_truce")}],
     "personnes": ["giorgia-meloni", "antonio-costa", "donald-trump"]},
    {"id": "bardella-mediapart", "titre": "Affaire Bardella – Mediapart", "ouvert": "2026-09-28", "maj": "2026-11-05",
     "resume": "Mediapart refoulé au lancement du livre de Bardella",
     "etat": [
         {"titre": "Les faits", "texte": "Mediapart attribue à Jordan Bardella des messages antisémites et publie ses éléments d’authentification, dont une extraction de conversation Messenger constatée par un commissaire de justice."},
         {"titre": "La réponse de Bardella", "texte": "Il conteste en être l’auteur, dénonce des faux et annonce des poursuites, notamment pour diffamation."}],
     "chrono": [
         {"date": "2026-11-04", "texte": "Un reporter de Mediapart est refoulé au lancement du livre de Jordan Bardella ; la plupart des journalistes quittent la soirée.", "sources": src("24m_livre", "yahoo_livre")},
         {"date": "2026-10-09", "texte": "Mediapart publie de nouveaux éléments à l’appui de l’authenticité des messages.", "sources": src("wiki_mediapart")},
         {"date": "2026-10-01", "texte": "Mediapart détaille comment il a authentifié les échanges.", "sources": src("wiki_mediapart")},
         {"date": "2026-09-28", "texte": "Première publication de Mediapart sur les messages attribués à Jordan Bardella.", "sources": src("f24_mediapart")}],
     "personnes": ["jordan-bardella"]},
    {"id": "attentat-trappes", "titre": "Attentat de Trappes", "ouvert": "2026-10-23", "maj": "2026-10-30",
     "resume": "Hommage national annoncé",
     "etat": [
         {"titre": "Les faits", "texte": "Le 23 octobre, un homme a tiré depuis sa voiture à Trappes et La Verrière (Yvelines), tuant Pengo Bossio Wangi, 26 ans, et blessant sept personnes, dont une fillette de 12 ans."},
         {"titre": "L’enquête", "texte": "Le parquet national antiterroriste s’est saisi. Le suspect, 39 ans, a été mis en examen pour assassinat terroriste à caractère raciste et écroué."},
         {"titre": "La suite", "texte": "Un hommage national présidé par Sébastien Lecornu a été annoncé ; sa date reste à préciser."}],
     "chrono": [
         {"date": "2026-10-30", "texte": "Rassemblement contre le racisme à Trappes ; le suspect est mis en examen et écroué.", "sources": src("pm_trappes")},
         {"date": "2026-10-28", "texte": "Le gouvernement annonce un hommage national présidé par Sébastien Lecornu.", "sources": src("iy_trappes")},
         {"date": "2026-10-23", "texte": "Fusillade à Trappes et La Verrière : un mort et sept blessés.", "sources": src("iy_trappes")}],
     "personnes": ["sebastien-lecornu", "laurent-nunez", "aurore-berge"]},
    {"id": "bordeaux-17-octobre", "titre": "Bordeaux après le 17 octobre", "ouvert": "2026-10-17", "maj": "2026-11-06", "region": "Bordeaux",
     "resume": "Le conseil municipal chiffre les dégâts",
     "etat": [
         {"titre": "Ce qui s’est passé", "texte": "Le 17 octobre, des émeutes ont éclaté en marge de la manifestation ; la résidence préfectorale a été saccagée et le RAID déclenché."},
         {"titre": "Le bilan", "texte": "La mairie chiffre à 350 000 € les dégâts pour la ville et la métropole, et à 8-10 M€ ceux des 81 commerces touchés."},
         {"titre": "Le débat local", "texte": "Thomas Cazenave demande que les cortèges évitent l’hypercentre ; l’opposition l’accuse de renier ses promesses sur la sécurité."}],
     "chrono": [
         {"date": "2026-11-02", "texte": "Conseil municipal : longs échanges tendus sur la sécurité et le droit de manifester.", "sources": src("rue89_cm", "gazette_cm")},
         {"date": "2026-10-17", "texte": "Émeutes en marge de la manifestation, résidence préfectorale saccagée, RAID déclenché.", "sources": src("sud_bordeaux")}],
     "personnes": ["thomas-cazenave", "pierre-hurmic"]},
    {"id": "biarritz-canon-francais", "titre": "Biarritz : le banquet du Canon français", "ouvert": "2026-10-14", "maj": "2026-11-05", "region": "Biarritz",
     "resume": "Un faux communiqué d’annulation circule",
     "etat": [
         {"titre": "L’événement", "texte": "Le Canon français organise un « banquet basque » à Biarritz le 28 novembre ; ses opposants l’accusent de banaliser l’extrême droite."},
         {"titre": "Sécurité", "texte": "La préfecture réclame 45 000 € aux organisateurs pour le dispositif des forces de l’ordre."},
         {"titre": "Contestation", "texte": "Cent personnalités du Pays basque appellent à former un « rempart humain » le jour du banquet."}],
     "chrono": [
         {"date": "2026-11-04", "texte": "Un faux communiqué annonçant l’annulation du banquet circule en ligne.", "sources": src("f3_biarritz")},
         {"date": "2026-10-30", "texte": "La préfecture réclame 45 000 € aux organisateurs.", "sources": src("ici_biarritz")},
         {"date": "2026-10-14", "texte": "Appel de cent personnalités à une chaîne humaine le 28 novembre.", "sources": src("f3_biarritz")}],
     "personnes": ["serge-blanco"]},
]}
dump("fils.json", fils)

# ---------------------------------------------------------------- personnes
P = lambda id, nom, fonction, camp, bio, parti="": {"id": id, "nom": nom, "fonction": fonction, "camp": camp, "parti": parti, "bio": bio}
personnes = {"schema": 1, "maj": "2026-11-06", "personnes": [
    P("emmanuel-macron", "Emmanuel Macron", "Président de la République", "Exécutif", "Élu en 2017, réélu en 2022 ; son second et dernier mandat s’achève en mai 2027.", "Renaissance"),
    P("sebastien-lecornu", "Sébastien Lecornu", "Premier ministre", "Exécutif", "Nommé le 9 septembre 2025, reconduit le 10 octobre 2025 ; gouvernement remanié le 26 février 2026. Il dit ne pas être candidat à la présidentielle.", "Renaissance"),
    P("laurent-nunez", "Laurent Nuñez", "Ministre de l’Intérieur", "Exécutif", "Ancien préfet de police de Paris. Emmanuel Macron a refusé sa démission le 19 octobre 2026, après les violences du 17 octobre."),
    P("gerald-darmanin", "Gérald Darmanin", "Ministre de la Justice", "Exécutif", "Garde des Sceaux, ancien ministre de l’Intérieur."),
    P("david-amiel", "David Amiel", "Ministre de l’Action et des Comptes publics", "Exécutif", "Porte le budget 2027 au Parlement."),
    P("maud-bregeon", "Maud Bregeon", "Porte-parole du gouvernement", "Exécutif", "Ministre déléguée, porte-parole du gouvernement et chargée de l’Énergie."),
    P("aurore-berge", "Aurore Bergé", "Ministre déléguée à l’Égalité femmes-hommes", "Exécutif", "Chargée de l’Égalité entre les femmes et les hommes et de la Lutte contre les discriminations."),
    P("yael-braun-pivet", "Yaël Braun-Pivet", "Présidente de l’Assemblée nationale", "Institutions", "Présidente de l’Assemblée depuis 2022.", "Renaissance"),
    P("philippe-juvin", "Philippe Juvin", "Rapporteur général du budget à l’Assemblée", "Institutions", "Député LR ; a justifié le rejet du budget au nom de la responsabilité et de la vérité dues aux Français.", "LR"),
    P("christine-lavarde", "Christine Lavarde", "Rapporteure générale du budget au Sénat", "Institutions", "Sénatrice LR ; juge irréaliste l’hypothèse de croissance de 1 % du gouvernement.", "LR"),
    P("marine-le-pen", "Marine Le Pen", "Candidate du RN à la présidentielle", "Extrême droite", "Présidente du groupe RN à l’Assemblée, déjà candidate en 2012, 2017 et 2022. Condamnée en appel le 7 juillet 2026 dans l’affaire des assistants parlementaires européens, avec une inéligibilité ferme réduite qui lui permet de se présenter.", "RN"),
    P("jordan-bardella", "Jordan Bardella", "Président du RN", "Extrême droite", "Réélu à la tête du parti le 24 octobre 2026 avec 98,98 % des voix ; eurodéputé. Conteste les messages que lui attribue Mediapart.", "RN"),
    P("jean-philippe-tanguy", "Jean-Philippe Tanguy", "Député RN", "Extrême droite", "Spécialiste des questions budgétaires au RN.", "RN"),
    P("eric-zemmour", "Éric Zemmour", "Président de Reconquête", "Extrême droite", "Candidat en 2022, de nouveau dans la course pour 2027.", "Reconquête"),
    P("nicolas-dupont-aignan", "Nicolas Dupont-Aignan", "Candidat souverainiste", "Droite", "Quatrième candidature consécutive à la présidentielle.", "Debout la France"),
    P("jean-luc-melenchon", "Jean-Luc Mélenchon", "Candidat de LFI à la présidentielle", "Gauche", "Fondateur de La France insoumise, deuxième des derniers sondages Ifop.", "LFI"),
    P("raphael-glucksmann", "Raphaël Glucksmann", "Candidat PS–Place publique", "Gauche", "Cofondateur de Place publique, eurodéputé. A remporté la primaire du PS, de Place publique et de la GRS le 11 octobre 2026 avec 66,17 %.", "Place publique"),
    P("olivier-faure", "Olivier Faure", "Premier secrétaire du PS", "Gauche", "Dirige le Parti socialiste.", "PS"),
    P("francois-ruffin", "François Ruffin", "Député de la Somme, président de Debout !", "Gauche", "Ancien député LFI, candidat à la présidentielle.", "Debout !"),
    P("marine-tondelier", "Marine Tondelier", "Secrétaire nationale des Écologistes", "Gauche", "Testée à 3-3,5 % dans le sondage Ifop de novembre.", "Les Écologistes"),
    P("fabien-roussel", "Fabien Roussel", "Secrétaire national du PCF", "Gauche", "Testé à 1,5-2 % dans le sondage Ifop de novembre.", "PCF"),
    P("clementine-autain", "Clémentine Autain", "Députée de Seine-Saint-Denis", "Gauche", "Figure de L’Après, promotrice d’une primaire unitaire de la gauche.", "L’Après"),
    P("edouard-philippe", "Édouard Philippe", "Président d’Horizons, candidat", "Centre", "Ancien Premier ministre, maire du Havre réélu en 2026, candidat déclaré depuis 2024.", "Horizons"),
    P("gabriel-attal", "Gabriel Attal", "Figure de Renaissance", "Centre", "Ancien Premier ministre (2024), testé dans les sondages pour 2027.", "Renaissance"),
    P("bruno-retailleau", "Bruno Retailleau", "Président des Républicains, candidat", "Droite", "Ancien ministre de l’Intérieur ; propose un référendum sur une règle d’or budgétaire.", "LR"),
    P("laurent-wauquiez", "Laurent Wauquiez", "Député LR", "Droite", "Battu par Bruno Retailleau pour la présidence de LR en 2025.", "LR"),
    P("david-lisnard", "David Lisnard", "Maire de Cannes, candidat", "Droite", "Ancien LR, candidat de droite libérale ; réclame une primaire ouverte de la droite et du centre."),
    P("natacha-polony", "Natacha Polony", "Candidate à la présidentielle", "Autres", "Journaliste, déclarée candidate mi-octobre 2026."),
    P("christine-lagarde", "Christine Lagarde", "Présidente de la BCE", "Institutions", "À la tête de la BCE depuis 2019, elle quittera ses fonctions le 7 février 2027, avant le terme de son mandat."),
    P("emmanuel-moulin", "Emmanuel Moulin", "Gouverneur de la Banque de France", "Institutions", "En poste depuis le 2 juin 2026, après le départ anticipé de François Villeroy de Galhau ; ancien secrétaire général de l’Élysée."),
    P("donald-trump", "Donald Trump", "Président des États-Unis", "International", "Son camp a perdu la Chambre et le Sénat aux élections de mi-mandat du 3 novembre 2026."),
    P("giorgia-meloni", "Giorgia Meloni", "Présidente du Conseil italien", "International", "Réclame un représentant unique de l’UE dans les négociations sur l’Ukraine."),
    P("antonio-costa", "António Costa", "Président du Conseil européen", "International", "Destinataire de la lettre de Giorgia Meloni sur l’Ukraine."),
    P("thomas-cazenave", "Thomas Cazenave", "Maire de Bordeaux", "Territoires", "Élu en mars 2026 avec 50,95 % face au maire écologiste sortant ; ancien député Renaissance.", "Renaissance"),
    P("pierre-hurmic", "Pierre Hurmic", "Conseiller municipal d’opposition à Bordeaux", "Territoires", "Maire écologiste de Bordeaux de 2020 à 2026.", "Les Écologistes"),
    P("alain-rousset", "Alain Rousset", "Président de la région Nouvelle-Aquitaine", "Territoires", "À la tête de la région depuis 2016 (de l’Aquitaine depuis 1998).", "PS"),
    P("germinal-peiro", "Germinal Peiro", "Président du conseil départemental de la Dordogne", "Territoires", "Président du département de la Dordogne.", "PS"),
    P("michel-cadet", "Michel Cadet", "Maire de Périgueux", "Territoires", "Élu en mars 2026 avec 53,21 % au second tour.", "Divers droite"),
    P("serge-blanco", "Serge Blanco", "Maire de Biarritz", "Territoires", "Ancienne légende du rugby, élu en mars 2026 avec 41,92 % au second tour.", "Divers centre"),
]}
dump("personnes.json", personnes)

# ---------------------------------------------------------------- glossaire
G = lambda id, titre, paras, theme: {"id": id, "titre": titre, "texte": paras, "theme": theme, "ajoute": "2026-11-06"}
glossaire = {"schema": 1, "entrees": [
    G("rejet-budget", "Que se passe-t-il quand l’Assemblée rejette le budget ?", [
        "Le texte part au Sénat dans sa version d’origine : les amendements votés par les députés disparaissent. Après le vote du Sénat, une commission mixte paritaire de 7 députés et 7 sénateurs cherche un compromis.",
        "En cas d’échec, l’Assemblée a le dernier mot et le gouvernement peut recourir au 49.3, au risque d’une motion de censure. Si le Parlement ne s’est pas prononcé en 70 jours, le budget peut passer par ordonnance (article 47). Sans budget au 1er janvier, une loi spéciale permet de continuer à lever l’impôt."], "Institutions"),
    G("article-49-3", "Article 49.3", [
        "Il permet au Premier ministre d’engager la responsabilité du gouvernement sur un texte. Le texte est adopté sans vote, sauf si une motion de censure, déposée dans les 24 heures, est votée par la majorité absolue des députés, soit 289 voix."], "Institutions"),
    G("motion-de-censure", "Motion de censure", [
        "Vote par lequel l’Assemblée peut renverser le gouvernement. Elle doit être signée par au moins un dixième des députés et adoptée à la majorité absolue des membres, soit 289 voix : seuls les votes pour sont comptés."], "Institutions"),
    G("commission-mixte-paritaire", "Commission mixte paritaire (CMP)", [
        "Sept députés et sept sénateurs chargés de trouver un texte commun quand les deux chambres ne sont pas d’accord. Si elle échoue, l’Assemblée a le dernier mot après une nouvelle lecture."], "Institutions"),
    G("loi-speciale", "Loi spéciale", [
        "Si le budget n’est pas adopté au 1er janvier, le gouvernement peut faire voter une loi spéciale qui l’autorise à continuer de percevoir les impôts existants, en attendant un vrai budget. La France y a eu recours fin 2024."], "Institutions"),
    G("recession-technique", "Récession technique", [
        "Deux trimestres consécutifs de baisse du PIB. En 2026, la France a enchaîné −0,2 %, 0,0 % puis −0,1 % : pas de récession technique au sens strict, mais neuf mois sans croissance."], "Économie"),
    G("spread-oat-bund", "Écart OAT-Bund (spread)", [
        "Différence entre le taux d’emprunt à 10 ans de la France (OAT) et celui de l’Allemagne (Bund), en points de base (1 pb = 0,01 point). Il mesure la prime de risque que les investisseurs exigent pour prêter à la France plutôt qu’à l’Allemagne.",
        "Au 5 novembre 2026, il était de 148 pb, proche de ses plus hauts depuis la crise de la zone euro de 2012."], "Marchés"),
    G("regle-d-or", "Règle d’or budgétaire", [
        "Principe qui impose l’équilibre des comptes publics, ou interdit qu’un budget augmente la dette. L’Allemagne a inscrit un « frein à l’endettement » dans sa Loi fondamentale en 2009.",
        "En France, une loi organique de 2012 encadre la trajectoire des finances publiques, sans règle d’or dans la Constitution. Le dernier budget voté à l’équilibre date de 1974."], "Économie"),
    G("taux-de-depot-bce", "Taux de dépôt de la BCE", [
        "Taux auquel la BCE rémunère les dépôts des banques ; c’est lui qui pilote la politique monétaire de la zone euro. Il est à 2,50 % depuis le 16 septembre 2026, après deux hausses dans l’année."], "Marchés"),
]}
dump("glossaire.json", glossaire)

# ---------------------------------------------------------------- séries
dump("chiffres.json", {"schema": 1, "series": {
    "cac40": [{"d": "2026-11-05", "v": 8205.37}],
    "oat10": [{"d": "2026-11-05", "v": 4.752}],
    "spread": [{"d": "2026-11-05", "v": 148.2}],
    "brent": [{"d": "2026-11-05", "v": 98.29}],
    "or": [{"d": "2026-11-05", "v": 4135}],
    "eurusd": [{"d": "2026-11-05", "v": 1.1227}],
}})
dump("sondages.json", {"schema": 1, "vagues": [dict(edition["sondage"])]})

# ---------------------------------------------------------------- index
dump("index.json", {
    "schema": 1,
    "maj": "2026-11-06T07:00:00+01:00",
    "derniere": "2026-11-06",
    "presidentielle": {"tour1": "2027-04-18", "tour2": "2027-05-02"},
    "editions": [{"date": "2026-11-06", "type": "quotidien", "titre": edition["titre"], "sujets": nb_sujets}],
})
print("ok", nb_sujets, "sujets")
