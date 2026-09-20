# Översättningsminne från språkgranskningar

Denna utgåva innehåller **176 319 poster och 177 042 segment i 139 projektminnen**.

JSONL i [data](data/) är källa till minnena i [catalogs](catalogs/). [stats.json](stats.json) redovisar verifierade antal. Dessa poster kompletterar de platta ekosystemminnena i förrådets rot och ska inte adderas till deras antal som om alla par vore nya.

Granskningsunderlagen inventerades den 20 september 2026. Den offentliga översättningssamlingen lästes vid revision `67e6d27877c9cfd6b6dbc74bd852b10bdbe09c3c` av [yeager/translations](https://github.com/yeager/translations). Senare arbete i andra pågående granskningar ingår inte automatiskt.

Underlaget omfattar individuella beslut i FreeCADs 36 filer, bekräftade rättelser från Translation Project, GNOME och Ubuntu-granskningen, tidigare granskade filleveranser samt ändrade tvåspråkiga poster i översättningssamlingens granskningscommits. Automatiska varningar utan språkbeslut räknas inte som granskade rättelser.

`publication_status` skiljer lokala rättelser, inskickade förslag, publiceringskvitton, granskade filleveranser och ändringar i granskningscommits åt. En granskad filleverans bevisar inte att varje oförändrad post har ett separat registrerat radbeslut. Ingen av dessa beteckningar innebär formellt godkännande i Crowdin eller Weblate. FreeCADs ordlista är lokalt granskad; helfilsimporten nekas av Crowdin för filformatet glossary.

Varje post innehåller projekt, komponent, ursprunglig kontext, källtext, svensk text, hänvisning och SHA-256 för granskningsunderlaget. En källa kan ha flera korrekta svenska översättningar. Välj utifrån projekt, betydelse och kontext; ersätt aldrig globalt enbart utifrån det engelska ordet. Metadata och kontrolltecken bevaras i exporterna.

## Användning

Importera en passande TMX-fil i ditt CAT-verktyg, exempelvis `catalogs/freecad.tmx`. Varje segment behåller projekt, komponent, kontext, gransknings-ID och publiceringsstatus som TMX-egenskaper. Pluralformer lagras som separata segment med `plural_index` och med engelsk pluraltext när underlaget innehåller den.

PO-filerna bevarar båda svenska pluralformerna. Deras `msgctxt` är en JSON-lista med projekt, komponent, ursprunglig kontext, källpostens ID och gransknings-ID. De är avsedda som sökbara minnen, inte som färdiga ersättningsfiler för respektive program. För direkt återanvändning måste ursprunglig kontext jämföras.

```sh
python3 scripts/reviewed.py        # kontrollera JSONL, PO, TMX och antal
python3 scripts/reviewed.py --write # återgenerera PO/TMX efter en dataändring
```

JSONL avgränsas med LF, inte med alla Unicode-radbrytningstecken. Det gör att exempelvis U+2028 i själva översättningstexten bevaras. XML-förbjudna kontrolltecken använder samma dokumenterade TMX-platshållare som förrådets befintliga exporter.

## Avgränsning och spårbarhet

Källtexter som saknades i publiceringskvitton återställdes med kvalificerade projekt- och sträng-ID:n från Crowdin-exporter och Weblates API. API-källan och dess kontrollsumma sparas i `source_evidence`. Källtext och översättning kopplas aldrig ihop enbart genom ordens position i en fil. `inventory.json` redovisar underlag, undantag och kompletterande lokala rättelser.

23 pluralposter i Bitwarden, en pluralpost i PCSX2 och 30 poster i Libre Menu Editor fick kompletterande lokala rättelser vid insamlingen. De har särskild publiceringsstatus och är inte rapporterade som uppladdade till respektive översättningsplattform. Kontrollsumman i `evidence` avser det lästa granskningsunderlaget, medan länken kan gå till projektets översättningsvy; en levande Crowdin- eller Weblate-sida är inte ett oföränderligt arkiv.

TMX-egenskapen `note_json` innehåller granskningsanteckningen som en JSON-sträng, så även historiska kontrolltecken kan bevaras utan ogiltig XML. PO-kommentaren `Review-note (JSON)` använder samma kodning. PO-exporten använder inga automatiska radbrytningar i kommentarer; även metadata jämförs vid återinläsning.
