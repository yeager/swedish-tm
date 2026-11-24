# Home Assistant: svensk översättningsminnesexport

Detta är en kontextbevarande ögonblicksbild av samtliga **icke arkiverade** strängar med både engelsk källa och svensk måltext i Lokalises fyra Home Assistant-projekt, hämtad den 24 november 2026:

| Komponent | Enheter | Segment |
|---|---:|---:|
| Core | 75 645 | 75 647 |
| Frontend | 11 274 | 11 274 |
| iOS Companion | 3 572 | 3 572 |
| Android Companion | 1 668 | 1 673 |

Varje PO-post har Lokalise-nyckel och engelsk respektive svensk översättnings-ID i kommentaren. TMX-filerna bevarar motsvarande metadata, kontext och kontrollsumma för den importerade komponentens råa JSONL-ögonblicksbild. Katalogerna är API-exporter från angivet datum och kompletterar de mindre, individuellt granskade kopiorna i `../../review-archive/catalogs/`. En exporterad post är en översättningsresurs och innebär inte att varje äldre sträng har fått en ny språkgranskning. Den aktuella snapshoten omfattar även de 240 Core-posterna radgranskade 9181–9420 den 24 november 2026.

Kör den reproducerbara exporten med:

```sh
# Antingen en tillfällig miljövariabel eller den säkra skrivbordsnyckelringen:
export LOKALISE_TOKEN='…'
# keyring.set_password("lokalise", "api_token", "…")
python3 scripts/home_assistant_export.py --fetch --write --validate

# Vid löpande Core-granskning kan enbart Core hämtas och valideras:
python3 scripts/home_assistant_export.py --component core --fetch --write --validate
```

`glossary-sv.json` innehåller den svenska Home Assistant-terminologi som ska vara gemensam för core, frontend, iOS och Android. Den bygger på den befintliga projektordlistan och de granskade svenska beslut som används i de aktuella komponenterna.

## Lokala granskningsförslag, 19 november 2026

[TMX-tillägget för Core](sv-home-assistant-core-proposals-20261119.tmx) är för närvarande tomt: de sju tidigare textförslagen har sparats och återlästs i Lokalise och förts till det verifierade tillägget. De fem tidigare Miele-förslagen har sparats och återlästs i Lokalise; se [ändringsloggen](https://github.com/yeager/translations/blob/main/Home-Assistant/Lokalise/2026-11-19/sparade-andringar-miele.md). Andra lokala förslag i granskningsrapporterna återstår. Tillägget kompletterar den oförändrade ögonblicksbilden från 24 oktober; välj kontext och kontrollera aktuell källtext innan ett förslag används.

## Verifiering 19 november 2026

De fyra katalogerna har kontrollerats mot sina arkiverade JSONL-underlag: samtliga PO- och TMX-par stämmer med respektive ögonblicksbild. Även varje TMX-segments komponent, nyckel, kontext och underlagets SHA-256 kontrollerades utan avvikelser. Detta verifierar den historiska exportens internkonsistens, inte att den motsvarar dagens Lokalise eller att varje översättning är språkligt korrekt. Ingen ny liveexport har genomförts vid denna kontroll.

## Verifierat tillägg från Lokalise, 19 november 2026

[Separat Core-TMX](sv-home-assistant-core-lokalise-verified-20261119.tmx) innehåller 2536 sparade och återlästa översättningar från 584 ändringsloggar, med fullständig nyckel och spårbar länk till respektive granskningsrapport. Elva poster från 20 november 2026 har återlästs från Lokalise och lagts till med statusen `saved-and-read-back`. Tillägget är en partiell uppdatering, inte en aktuell fullständig export; de övriga senare Lokalise-ändringarna återstår att föra in och verifiera. De äldre katalogerna och det separata förslagsminnet är oförändrade. XML-struktur, unika nycklar, språkpar, platshållare och länkmål kontrollerades före publicering.

En separat livekontroll via Lokalises API den 19 november omfattade samtliga 75 007 Core-nycklar på 151 sidor och fann inga engelska nycklar med tom svensk översättning. Resultatet gäller täckning av fält, inte språklig kvalitet eller en ny fullständig TM-export.

Återställda nyckelreferenser förs inte in som vanliga textpar: referensernas ursprung och mål dokumenteras i ändringsloggarna och måste bedömas i sitt sammanhang.

## Löpande Core-granskning, 24 november 2026

Den aktuella Core-snapshoten innehåller 75 645 Lokalise-nycklar och har 75 647 segment efter de senaste fullständiga API-hämtningarna och de 17 nya översättningarna den 24 november 2026. PO och TMX har genererats från samma JSONL-underlag och validerats mot varandra. Granskningsstatusar och källor sparas i snapshoten; en ny hämtning bevarar status bara när den engelska källan och den svenska måltexten fortfarande är identiska. Ändras ett livevärde efter granskning, markeras posten `needs-review-live-change` i stället för att det gamla godkännandet följer med.

Lokalise kan representera en svensk pluralöversättning som ett JSON-objekt med `one` och `other`. `scripts/update_lokalise_batch.py` accepterar då formen `{"key_id":{"one":"…","other":"…"}}`, skickar rätt pluralpayload och återläser resultatet. Core-exportören tar även pluralformerna från aktuell komponent-`strings.json` när källans `other`-form saknas i API men Core-källan har en annan namngiven form, till exempel `two`. Detta gör att TMX och PO behåller rätt käll-/målpar.

## Nycklar utan användbart käll-/målpar

`snapshots/core-excluded.jsonl` dokumenterar nycklar som inte kan representeras som svensk-engelska par, med orsak och synlighetsstatus. Därmed faller inte tomma värden eller felaktiga pluralpar bort ur inventeringen. Core-exporten den 24 november 2026 innehåller 75 645 översatta enheter och 32 exkluderade, synliga nycklar: 24 utan text på någotdera språket och 8 utan engelsk källtext, men med svenska platshållarvärden. De 17 nya synliga nycklarna med tom svenska har översatts och flyttats till snapshoten. `scripts/home_assistant_export.py --validate --component core` kontrollerar exkluderingsinventeringen tillsammans med PO- och TMX-snapshoten.
## Radgranskning 22681–22800, 24 november 2026

Arbetet finns i `Home-Assistant/2026-11-24-reviewed-core-22681-22800.json` och den fullständiga rapporten i yeager/translations. 17 ändringar sparades och lästes tillbaka från Lokalise; en PM2.5-översättning granskades och behölls. Tre sökvägar saknar motsvarighet i aktuell Core-källa och har separat uppföljningsstatus. Den kanoniska manuellt verifierade TMX-filen innehåller nu 16 458 poster.

Nästa intervall, 22801–22920, granskades 24 november 2026. Elva ändringar sparades och återlästes; en referensnyckel kräver källsökvägsuppföljning. Rapport och manifest finns i yeager/translations och `Home-Assistant/2026-11-24-reviewed-core-22801-22920.json`. Den manuellt verifierade Core-TMX-filen innehåller 16 458 poster.

Core-intervallet 22921–23040 granskades 24 november 2026. Tio ändringar sparades och återlästes i Lokalise; alla tio källsökvägar verifierades i aktuell Core-källa. Rapport och manifest finns i yeager/translations och `Home-Assistant/2026-11-24-reviewed-core-22921-23040.json`. Den manuellt verifierade Core-TMX-filen innehåller 16 458 poster.

Core-intervallet 23041–23160 granskades 24 november 2026. Tolv ändringar sparades och återlästes; två befintliga mål verifierades och behölls. Alla 14 sökvägar matchar aktuell Core-källa. Rapport och manifest finns i yeager/translations och `Home-Assistant/2026-11-24-reviewed-core-23041-23160.json`. Core-TMX innehåller 16 458 poster.

Core-intervallet 23161–23280 granskades 24 november 2026. Tretton ändringar sparades och återlästes. Sex nyckelsökvägar kräver ytterligare referens-/ursprungskontroll; övriga sju matchar källan direkt. Rapport och manifest finns i yeager/translations och `Home-Assistant/2026-11-24-reviewed-core-23161-23280.json`. Core-TMX innehåller 16 458 poster.

Core-intervallet 23281–23400 granskades 24 november 2026. Tio värden korrigerades och lästes tillbaka; fyra befintliga värden bekräftades. Nio sökvägar kräver referens- eller ursprungskontroll. Rapport och manifest finns i yeager/translations och `Home-Assistant/2026-11-24-reviewed-core-23281-23400.json`. Core-TMX innehåller 16 458 poster.
