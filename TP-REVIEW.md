# Swedish TP review, 2026-09-23

This update records the complete requested review scope except Wastesedge. Of
Translation Project’s 127 367 active Swedish entries, 126 157 were individually
read. The remaining 1 210 Wastesedge entries were explicitly excluded because
the domain has not had a release for many years; they are not claimed as
reviewed.

`sv-tp.po` and `sv-tp.tmx` are updated from the pinned Swedish TM baseline
`c7ffe37c3108157e040dba478e15ae3d82bc7800`. The import makes 33 484 exact
English/source-domain/previous-Swedish-target matches and applies their verified
revised Swedish target in both formats. It does not guess from source text alone.

184 verified plural corrections remain outside this export because the
compendium represents only context-free singular pairs. Five XML-forbidden
control-character occurrences are preserved losslessly in TMX with documented
`<ph x="…" type="x-control">U+NNNN</ph>` placeholders; their PO counterparts
retain the original characters.

[The audit](reviews/tp-2026-09-23.json) contains every imported pair, excluded
plural correction and output digest. Validation checks GNU gettext syntax, XML
structure, exact PO/TMX pair agreement and regenerated repository statistics.
The [Translation Project Swedish team](https://translationproject.org/team/sv.html)
and [Swedish FOSS Terminology](https://github.com/yeager/swedish-foss-terminology)
provide review context.
