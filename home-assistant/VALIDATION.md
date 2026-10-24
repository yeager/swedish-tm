# Kontrollresultat, 24 oktober 2026

Exporten kontrollerades med `msgfmt --check`, den inbyggda XML/PO-jämförelsen i `scripts/home_assistant_export.py --validate` och en scoped Gitleaks-skanning av hela katalogen. Samtliga format- och säkerhetskontroller passerade.

| Komponent | l10n-lint | svlang-träffar | Hunspell, unika okända ord |
|---|---|---:|---:|
| core | 54 error(s), 886 warning(s) | 136 | 7903 |
| frontend | 5 error(s), 114 warning(s) | 32 | 876 |
| ios | 3 error(s), 46 warning(s) | 24 | 381 |
| android | 0 error(s), 32 warning(s) | 10 | 201 |

`l10n-lint`, `svlang` och Hunspell kördes mot hela den aktuella Lokalise-ögonblicksbilden. Resultaten är kvalitetsindikatorer för äldre befintliga översättningar, inte exportfel. Exporten återger därför dem exakt och påstår inte att de redan är åtgärdade eller individuellt omgranskade.

`glossary-coverage.json` jämför den gemensamma svenska terminologikandidaten med de fyra befintliga Lokalise-ordlistorna. Lokalise API svarade `401 Forbidden` på försök att skapa eller uppdatera termer, och Lokalise-gränssnittet visar ordlistefält som skrivskyddade för kontot. Kandidaten kan appliceras när kontot har behörigheten **Manage glossary**.

`git diff --check` rapporterar bevarade avslutande blanktecken i några importerade käll- och målsträngar. De ändras inte i minnesexporten, eftersom den måste vara en exakt återgivning av Lokalise-posterna.
