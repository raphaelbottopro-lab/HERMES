"""Reconstruit l'appli HERMÈS à la racine du dépôt à partir de dev/src.
Produit : index.html, sw.js, manifest.webmanifest. Les icônes (icons/) et les données (data/) ne sont pas touchées.
Usage, depuis la racine du dépôt : python3 dev/tools/build_app.py
Pour changer l'appli : modifier dev/src/app.html (fragment sans <html>/<head>) ou dev/src/sw.js, puis relancer ce script.
Penser à augmenter VERSION dans dev/src/app.html à chaque changement."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "dev" / "src"

frag = (SRC / "app.html").read_text(encoding="utf-8")
version = re.search(r"var VERSION = '([^']+)'", frag).group(1)

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Brief quotidien de l’actualité politique, économique et sociale française, et suivi du PLF 2027.">
<meta name="theme-color" content="#EDF1F7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1524" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="HERMÈS">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<style>:root{color-scheme:light dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
<script>window.HERMES_PWA=true;</script>
"""

MANIFEST = {
    "name": "HERMÈS", "short_name": "HERMÈS", "lang": "fr", "dir": "ltr",
    "description": "Brief quotidien de l’actualité politique, économique et sociale française, et suivi du PLF 2027.",
    "start_url": "./?source=pwa", "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": "#0D1524", "theme_color": "#0D1524",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}

m = re.search(r"(<title>.*?</title>\s*<meta[^>]*>\s*<style>.*?</style>)(.*)", frag, re.S)
html = HEAD + m.group(1) + "\n</head>\n<body>" + m.group(2) + "</body>\n</html>\n"
(ROOT / "index.html").write_text(html, encoding="utf-8")
(ROOT / "sw.js").write_text((SRC / "sw.js").read_text(encoding="utf-8").replace("__VERSION__", version), encoding="utf-8")
(ROOT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"HERMÈS {version} reconstruit dans {ROOT}")
