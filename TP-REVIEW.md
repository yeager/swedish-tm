# Swedish TP review, 2026-09-18

This is an ongoing complete language review of Translation Project's 146 Swedish domains. 33,100 of 127,367 active entries have been individually read. The review is not complete. This update corrects 9,445 confirmed English–Swedish pairs in both `sv-tp.po` and `sv-tp.tmx`.

The update is based on current main at `359390fce7a17db50de4722db14331cb9e9735b2`. Its export repairs, control-code conventions, project attribution and CC BY 4.0 licensing are retained. Other ecosystem exports are untouched. Two raw vertical-tab representations in the TP PO are escaped without changing their decoded text.

Each correction is matched against the English source, exact previous Swedish wording and the original TP project. No fuzzy matching or cross-project replacement is used. Exported memories lack gettext message context, so a candidate is excluded if its matching TP source/translation occurs in an entry that has not yet been read. 45 reviewed plural corrections have no corresponding entry in this singular compendium and are not added as invented records.

The review considers meaning, Swedish terminology and idiom. Routine English “please” is normally omitted in a direct Swedish instruction. Source code and documentation are checked where necessary; the termbank and existing memory are evidence, not automatic authorities. Denemo is still in progress; its individually reviewed corrections are included here.

All 117,723 TP units remain present. Every changed and unchanged unit is reread against its expected source, target and project provenance. The PO and TMX corrections match exactly. The project's full validator checks all 15 PO and 14 TMX exports, including GNU gettext, XML structure, identical pair inventories and regenerated statistics. Independent SHA-256 checks confirm the resulting TP files. The validator's nine tests pass.

[Change audit](reviews/tp-2026-09-18.json) records each previous and new translation, reason and original TP entry identifier. [Translation Project Swedish team](https://translationproject.org/team/sv.html), [Swedish FOSS terminology](https://github.com/yeager/swedish-foss-terminology) and project documentation provide review context.
