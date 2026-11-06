"""Assemble HERMÈS :
- dist/site/    : le site complet pour GitHub Pages (index.html, sw.js, manifeste, icônes, données)
- dist/preview/ : la même appli sans service worker, pour l'aperçu en artefact
Usage : python3 tools/build_app.py"""
import json, re, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC, DATA, LOGO = ROOT / "src", ROOT / "app" / "data", ROOT / "logo"
DIST = ROOT / "dist"

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

def icons(dst):
    (dst / "icons").mkdir(parents=True, exist_ok=True)
    for f in ["icon-192.png", "icon-512.png", "apple-touch-icon.png"]:
        shutil.copy(LOGO / f, dst / "icons" / f)
    Image.open(LOGO / "hermes-logo-256.png").resize((128, 128), Image.LANCZOS).save(dst / "icons" / "logo.png", optimize=True)

def data(dst):
    shutil.copytree(DATA, dst / "data", dirs_exist_ok=True)

def build_site():
    dst = DIST / "site"
    shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
    # Le fragment commence par <title> et <meta> : on les garde dans le <head>, le reste va dans <body>
    m = re.search(r"(<title>.*?</title>\s*<meta[^>]*>\s*<style>.*?</style>)(.*)", frag, re.S)
    head_part, body_part = m.group(1), m.group(2)
    html = HEAD + head_part + "\n</head>\n<body>" + body_part + "</body>\n</html>\n"
    (dst / "index.html").write_text(html, encoding="utf-8")
    (dst / "sw.js").write_text((SRC / "sw.js").read_text(encoding="utf-8").replace("__VERSION__", version), encoding="utf-8")
    (dst / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1), encoding="utf-8")
    (dst / ".nojekyll").write_text("")
    icons(dst); data(dst)
    return dst

def build_preview():
    dst = DIST / "preview"
    shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
    (dst / "index.html").write_text(frag, encoding="utf-8")
    icons(dst); data(dst)
    return dst

if __name__ == "__main__":
    s, p = build_site(), build_preview()
    n = sum(1 for _ in (s / "data").rglob("*.json"))
    print(f"HERMÈS {version} : site -> {s} ; aperçu -> {p} ; {n} fichiers de données")
