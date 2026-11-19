# Home Assistant: svensk översättningsminnesexport

Detta är en kontextbevarande ögonblicksbild av samtliga **icke arkiverade** strängar med både engelsk källa och svensk måltext i Lokalises fyra Home Assistant-projekt, hämtad den 24 oktober 2026:

| Komponent | Enheter | Segment |
|---|---:|---:|
| Core | 70 104 | 70 105 |
| Frontend | 11 274 | 11 274 |
| iOS Companion | 3 572 | 3 572 |
| Android Companion | 1 668 | 1 673 |

Varje PO-post har Lokalise-nyckel och engelsk respektive svensk översättnings-ID i kommentaren. TMX-filerna bevarar motsvarande metadata, kontext och kontrollsumma för den importerade komponentens råa JSONL-ögonblicksbild. Katalogerna är API-exporter från angivet datum och kompletterar den mindre, individuellt granskade `reviewed/catalogs/home-assistant.*`-katalogen. En exporterad post är en översättningsresurs och innebär inte att varje äldre sträng har fått en ny språkgranskning.

Kör den reproducerbara exporten med:

```sh
export LOKALISE_TOKEN='…'
python3 scripts/home_assistant_export.py --fetch --write --validate
```

`glossary-sv.json` innehåller den svenska Home Assistant-terminologi som ska vara gemensam för core, frontend, iOS och Android. Den bygger på den befintliga projektordlistan och de granskade svenska beslut som används i de aktuella komponenterna.

## Lokala granskningsförslag, 19 november 2026

[TMX-tillägget för Core](sv-home-assistant-core-proposals-20261119.tmx) innehåller för närvarande inga poster. De fem tidigare Miele-förslagen har sparats och återlästs i Lokalise; se [ändringsloggen](https://github.com/yeager/translations/blob/main/Home-Assistant/Lokalise/2026-11-19/sparade-andringar-miele.md). Andra lokala förslag i granskningsrapporterna återstår. Tillägget kompletterar den oförändrade ögonblicksbilden från 24 oktober; välj kontext och kontrollera aktuell källtext innan ett förslag används.

## Verifiering 19 november 2026

De fyra katalogerna har kontrollerats mot sina arkiverade JSONL-underlag: samtliga PO- och TMX-par stämmer med respektive ögonblicksbild. Även varje TMX-segments komponent, nyckel, kontext och underlagets SHA-256 kontrollerades utan avvikelser. Detta verifierar den historiska exportens internkonsistens, inte att den motsvarar dagens Lokalise eller att varje översättning är språkligt korrekt. Ingen ny liveexport har genomförts vid denna kontroll.

## Verifierat tillägg från Lokalise, 19 november 2026

[Separat Core-TMX](sv-home-assistant-core-lokalise-verified-20261119.tmx) innehåller 342 sparade och återlästa översättningar från femtiotre ändringsloggar, med fullständig nyckel och källhänvisning inklusive källfilens Git-blob. De fyra tidigare posterna är oförändrade. Tillägget är en partiell uppdatering, inte en aktuell fullständig export; de övriga senare Lokalise-ändringarna återstår att föra in och verifiera. De äldre katalogerna och det separata förslagsminnet är oförändrade. XML-struktur, unika nycklar, språkpar, platshållare och länkmål kontrollerades före publicering.

Återställda nyckelreferenser förs inte in som vanliga textpar: referensernas ursprung och mål dokumenteras i ändringsloggarna och måste bedömas i sitt sammanhang.
