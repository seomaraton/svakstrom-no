# svakstrom.no

Statisk informasjonsnettsted om svakstrøm og sterkstrøm. Ren HTML og CSS, ingen JavaScript, ingen informasjonskapsler, ingen eksterne tjenester.

## Struktur

```
build.py              Byggeskript (Python 3, ingen avhengigheter)
src/layout.html       Felles ramme: topp, meny, bunn
src/pages/*.html      Én fil per side, med metadata øverst
src/static/           CSS, skrifttyper og favicon (kopieres uendret)
public/               Ferdig nettsted. Det er denne mappen som legges ut.
```

## Bygge og se på siden

```
python3 build.py
python3 -m http.server 8000 --directory public
```

Åpne deretter http://localhost:8000

Byggeskriptet stopper med en feilmelding hvis en side lenker til en side som ikke finnes, eller viser til en kilde som mangler i `kilder.html`.

## Redigere innhold

- Hver side starter med en kommentarblokk med `title:` og `description:`.
- Kildehenvisninger skrives som `[[4]]` eller `[[4,13]]`. De blir til lenker til `kilder.html#k4`.
- Ny kilde: legg til en `<li id="kNN">` nederst i `src/pages/kilder.html`.
- Ny side: lag filen i `src/pages/` og legg den eventuelt inn i `NAV` i `build.py`.

## Legge ut

Nettstedet ligger på GitHub Pages. Hver push til `main` bygger og publiserer automatisk via `.github/workflows/pages.yml`.

- Domenet svakstrom.no er registrert hos Feno, og DNS peker til GitHub Pages.
- `src/static/CNAME` forteller GitHub hvilket domene siden skal svare på.
- `public/` er generert og ligger ikke i Git.

## Før publisering

- [ ] Legg eventuelt til utgiver og kontaktadresse i `src/pages/om.html`.
- [ ] Kontroller paragrafhenvisninger mot Lovdata, se «Om kildegrunnlaget» på kildesiden.

## Skrifttyper

IBM Plex Sans, IBM Plex Sans Condensed og IBM Plex Mono, lisensiert under SIL Open Font License 1.1. Filene ligger lokalt i `src/static/fonts/`.
