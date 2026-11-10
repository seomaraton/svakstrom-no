#!/usr/bin/env python3
"""Bygger svakstrom.no fra src/ til public/. Ingen avhengigheter utover Python 3.

Bruk:  python3 build.py

Hver fil i src/pages/ starter med en kommentarblokk med metadata:

    <!--
    title: Sidetittel
    description: Kort beskrivelse til søkemotorer
    -->

I brødteksten blir [[4]] og [[4,13]] gjort om til kildehenvisninger
som lenker til kilder.html#k4 osv.
"""
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "public"
SITE = "https://svakstrom.no"

NAV = [
    ("hva-er-svakstrom", "Hva er svakstrøm"),
    ("svakstrom-og-sterkstrom", "Svak og sterk"),
    ("anlegg", "Anlegg"),
    ("sikkerhet", "Sikkerhet"),
    ("regelverk", "Regelverk"),
    ("gjor-det-selv", "Egeninnsats"),
    ("utdanning", "Utdanning"),
    ("ordliste", "Ordliste"),
]


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    if not m:
        sys.exit(f"{path.name}: mangler metadatablokk øverst")
    meta = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def cites(body: str, known: set, page: str) -> str:
    def repl(m):
        nums = [n.strip() for n in m.group(1).split(",")]
        for n in nums:
            if n not in known:
                sys.exit(f"{page}: kilde [[{n}]] finnes ikke i kilder.html")
        links = ", ".join(f'<a href="kilder.html#k{n}">{n}</a>' for n in nums)
        return f'<sup class="cite">{links}</sup>'
    return re.sub(r"\[\[([\d,\s]+)\]\]", repl, body)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "static", OUT)

    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    pages = sorted((SRC / "pages").glob("*.html"))
    known = set(re.findall(r'id="k(\d+)"', (SRC / "pages" / "kilder.html").read_text(encoding="utf-8")))
    slugs = {p.stem for p in pages}
    today = date.today().isoformat()
    urls = []

    for path in pages:
        slug = path.stem
        meta, body = parse(path)
        body = cites(body, known, path.name)

        for href in re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', body):
            if Path(href).stem not in slugs:
                sys.exit(f"{path.name}: lenke til {href} som ikke finnes")

        current = ' aria-current="page"'
        nav = "\n".join(
            f'          <li><a href="{s}.html"{current if s == slug else ""}>{label}</a></li>'
            for s, label in NAV
        )
        title = meta["title"]
        full_title = "Svakstrøm.no" if slug == "index" else f"{title} | Svakstrøm.no"
        canonical = f"{SITE}/" if slug == "index" else f"{SITE}/{slug}.html"
        html = (layout
                .replace("{{full_title}}", full_title)
                .replace("{{description}}", meta["description"])
                .replace("{{canonical}}", canonical)
                .replace("{{nav}}", nav)
                .replace("{{body_class}}", f"page-{slug}")
                .replace("{{content}}", body.strip())
                .replace("{{year}}", str(date.today().year)))
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        if slug != "404":
            urls.append(canonical)

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"Bygget {len(pages)} sider til {OUT}")


if __name__ == "__main__":
    main()
