# HERMÈS

Appli perso (PWA iPhone) : brief quotidien de l'actualité politique, économique et sociale française, fils suivis dans la durée, suivi du PLF 2027 et fiches « Savoir ».

- Appli : https://raphaelbottopro-lab.github.io/HERMES/
- `index.html`, `sw.js`, `manifest.webmanifest`, `icons/` : l'appli publiée (générée par `dev/tools/build_app.py` à partir de `dev/src/`).
- `data/` : les données, écrites chaque matin par les tâches planifiées (format dans `dev/SCHEMA.md`).
- `dev/tools/check_data.py` : contrôle des données, à lancer avant chaque publication.
