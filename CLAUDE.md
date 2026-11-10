# Prosjektnotater for Claude Code

Statisk nettsted for svakstrom.no. Les README.md for struktur og kommandoer.

## Regler for innhold

- Språk: norsk bokmål. Korte, direkte setninger.
- Tone: saklig og nøktern. Bare fakta. Ingen humor, retoriske spørsmål, slagord eller utropstegn. Overskrifter skal beskrive innholdet.
- Hver faktaopplysning (tall, grense, dato, regel) skal ha kildehenvisning med `[[n]]`.
- Skriv med egne ord. Ikke kopier tekst fra kildene.
- Skill mellom gjeldende rett og historiske definisjoner. FEF 1987 (kilde 3) er opphevet.
- Svak/sterk handler om formål og fare. Lav/høy handler om spenningsnivå. Ikke bland dem.

## Regler for kode

- Rediger bare i `src/`. `public/` er generert og overskrives av `python3 build.py`.
- Ingen JavaScript, ingen eksterne ressurser, ingen sporing.
- Alle farger går via CSS-tokens i `:root`. Svakstrøm bruker `--svak`, sterkstrøm bruker `--sterk`.
- Brede tabeller og figurer skal ligge i `<div class="scroll">`.
- Kjør `python3 build.py` etter hver endring. Skriptet validerer lenker og kildehenvisninger.

## Publisering

- Push til `main` publiserer til GitHub Pages på svakstrom.no. Ikke commit `public/`.
