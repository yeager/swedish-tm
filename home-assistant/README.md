# Home Assistant: svensk översättningsminnesexport

Detta är en kontextbevarande ögonblicksbild av samtliga **icke arkiverade** strängar med både engelsk källa och svensk måltext i Lokalises fyra Home Assistant-projekt, hämtad den 24 oktober 2026:

| Komponent | Enheter | Segment |
|---|---:|---:|
| Core | 70 104 | 70 105 |
| Frontend | 11 274 | 11 274 |
| iOS Companion | 3 572 | 3 572 |
| Android Companion | 1 668 | 1 673 |

Varje PO-post har Lokalise-nyckel och engelsk respektive svensk översättnings-ID i kommentaren. TMX-filerna bevarar motsvarande metadata, kontext och kontrollsumma för den importerade komponentens råa JSONL-ögonblicksbild. Katalogerna är aktuella API-exporter och kompletterar den mindre, individuellt granskade `reviewed/catalogs/home-assistant.*`-katalogen. En exporterad post är en översättningsresurs och innebär inte att varje äldre sträng har fått en ny språkgranskning.

Kör den reproducerbara exporten med:

```sh
export LOKALISE_TOKEN='…'
python3 scripts/home_assistant_export.py --fetch --write --validate
```

`glossary-sv.json` innehåller den svenska Home Assistant-terminologi som ska vara gemensam för core, frontend, iOS och Android. Den bygger på den befintliga projektordlistan och de granskade svenska beslut som används i de aktuella komponenterna.
