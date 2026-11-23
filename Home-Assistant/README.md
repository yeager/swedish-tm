# Home Assistant

Den här katalogen samlar allt Home Assistant-material i `swedish-tm`.

* Filerna i rotkatalogen är den aktiva Lokalise-ledgern: sparade och
  återlästa ändringar, batchmanifest och den kanoniska Core-TMX:en.
* `source-archive/home-assistant/` innehåller de importerade PO/TMX-filerna,
  snapshots och tidigare granskningsunderlag. De är historiska källor, inte
  den aktuella Lokalise-sanningen.
* `review-archive/` innehåller de äldre, generella granskningskopiorna som
  tidigare låg under `reviewed/`.

Den aktuella Core-TMX:en är
`sv-home-assistant-core-lokalise-verified-20261120-canonical.tmx`. Validera
den med:

```bash
python3 scripts/validate_home_assistant_core_tmx.py \
  Home-Assistant/sv-home-assistant-core-lokalise-verified-20261120-canonical.tmx
```

Nya Lokalise-granskningar ska läggas i rotkatalogen tillsammans med sitt
verifierade manifest och sedan föras in i den kanoniska TMX:en.
