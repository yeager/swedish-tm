# Gnumeric help Hunspell exceptions — 2026-11-25

The Swedish dictionary reported these terms in reviewed help batches 77–78. Each was checked in context:

- **Hyndman** — surname in the Hyndman–Fan statistical method.
- **AMORtissement DEGRessif Comptabilite** — French source wording explaining the `AMORDEGRC` function name; retained as a source-specific name.
- **Pechtl** — author surname in the citation for `OPT_TIME_SWITCH`.
- **Black–Scholes / Scholes** — established model name.
- **vega** — established name of an option sensitivity, also a Greek letter.

XML entity fragments such as `&gt;` and `&lt;` were excluded from spelling checks. No other unknown prose words remain in these two batches.

Additional terms in batch 79:

- **Sheet1** — sheet reference in spreadsheet examples.
- **Lilliefors** and **Kolmogorov–Smirnov** — names of statistical tests.
- **principalkomponentanalys / principalkomponentanalysen** — statistical method name; valid Swedish compound.

Batch 80 preserves the sample chart category labels **Gadgets** and **Lumpets** because they name values shown in the figure.

Batch 81 preserves the example category labels **Gadgets** and **Lumpets** used in the bar-chart screenshot.

Batch 82 preserves the example category labels **Gadgets** and **Lumpets** in the pie/ring chart descriptions. The source ring-chart caption itself says first that the example uses one series and then that it uses three; the Swedish text preserves both source statements.

Additional term in batch 90:

- **t-test / t-testet** — standard Swedish label for Student's t-test; Hunspell does not recognize the letter-plus-hyphen compound.

Additional compound form in batch 91:

- **z-testverktyget** — Swedish compound for the z-test tool; Hunspell reports the hyphen boundary as a spelling error.

Additional statistical terms in batch 93:

- **ensvansad / ensvansat / ensvansade** and **tvåsvansat / tvåsvansade** — standard Swedish statistical terms used in existing GNOME TM table headings for one-tailed and two-tailed tests.
- **F-värde / F-kritiskt-värde** — statistical F-value terminology; Hunspell flags the letter-plus-hyphen compounds.
- **F-testverktyget / t-testet** — names of the statistical tools and tests.
- **1-faktors-ANOVA** — compact statistical heading with the number and technical acronym.

Additional statistical compounds in batch 94:

- **tvåfaktors-ANOVA / 2-faktors-ANOVA** — standard compound for two-factor analysis of variance; Hunspell splits the hyphenated form.

Additional help compounds in batch 95:

- **kontingenstabell** — standard Swedish statistical term for a contingency table.
- **cirkeldiagram / stapeldiagram / kolumndiagram** — established Swedish chart names; Hunspell splits these compounds when adjacent markup is stripped.

Technical names in batch 102:

- **gdk-pixbuf** — library name and filename, preserved as a technical identifier.
- **Sun raster**, **Scalable Vector Graphics**, and the listed image-format abbreviations — standard format names and identifiers retained in the help text.
- Batch 104 (Gnumeric image saving): `Gnumeric` is the application name; `PNG` is a standard image format.
- Batch 105 (deleting images and GUI components): `Gnumeric` is the application name.
- Batch 108 (checkboxes): `TRUE` and `FALSE` are Gnumeric Boolean literals kept exactly as source identifiers; `Gnumeric` is the application name.
- Batch 113 (drawing elements): `ritobjekt` and inflected forms are the chosen term for Gnumeric's simple graphical drawing objects; `Gnumeric` and `SVG` are application/format identifiers.
- Batch 114 (line and arrow drawing): `pilobjekt` is the chosen term for a graphical arrow drawing element.
- Batch 115 (arrow dimensions and rectangles): `ytfigurer` is used for area-shaped drawing objects; `Pilbredd` is the concise Swedish control name for Arrow Width.
- Batch 119 (graph terminology): `rittyp` and forms are the selected Swedish term for Gnumeric's distinct plot component; `Gnumeric` is the application name.
- Batch 120 (graph hierarchy): `X-Axis2` is an exact Gnumeric element identifier; `Gnumeric` is the application name; `rittyper` follows the documented graph terminology.
- Batch 121 (legends and diagram-guide panels): `XY-spridningsdiagram` is the standard plot-type name; `Gnumeric` is the application name.
- Batch 126 (plot configuration and area plot introduction): `Ytdiagram` is the selected Swedish chart-type term; `Gnumeric` and `rittyp` forms are covered by the existing exceptions above.
- Batch 127 (area plots): `Ytdiagram` and inflections are the established chart-type term; `Gadgets` and `Lumpets` remain exact sample-data labels matching the screenshot and table values.


Batch 130 identifiers flagged by Hunspell:

- **myCellRange** and **my_E_Constant** — example named range and constant from the Gnumeric help; preserved as exact identifiers. Hunspell splits the underscore identifier into `my` and `Constant`.


Batch 131:

- **Gnumeric** — application name, preserved in the file-opening instructions.


Batch 133 identifiers flagged by Hunspell:

- **user_account_name** — literal placeholder in the path example, preserved exactly; Hunspell splits it into `user`, `account` and `name`.
- **currentWork** — example folder name from the figure, preserved exactly.


Batch 136 technical terms:

- **CSV/TSV** — standard file-format abbreviations retained in the Gnumeric text import option labels.


Batch 140:

- **Insticksmodulhanteraren** — established Swedish UI name used in the GNOME TM for Plugin Manager; retained consistently although Hunspell does not recognize the compound.


Batch 145 technical names:

- **ASCII** — standard character encoding acronym; retained exactly.


Batch 146 sample value:

- **Dodji** — personal name in the source example value `Zoe, Sally, Dodji`, retained exactly.

Batch 158 example labels:

- **Gadgets**, **Lumpets** — sample category labels visible in the source screenshot; retained so the caption matches the image.

Batch 162 surface-plot notation:

- **Ytdiagram** — Swedish compound used for Gnumeric's surface chart type.
- **xy**, **xyz** — coordinate-plane and coordinate-series notation retained from the technical examples.

Batch 163 chart terminology:

- **XY-spridningsdiagram** — compound chart-type name retaining the standard XY coordinate designation.

Batch 164 sample code and references:

- **Sheet1**, **A2:B4**, **-1** — worksheet reference and numeric setting from documented examples; retained exactly.

Batch 166 formula notation:

- **9N** — part of the source formula expression `9N−1` for allowed minor-tick values; preserved exactly.

Batch 168 worksheet references:

- **D7**, **E7:I7**, **E6:I6** — spreadsheet cell/range references in a source example; preserved exactly.

Batch 170 documents the following Hunspell exceptions, checked in context:

- **SeriesName** — literal example string in the manual; retained exactly as sample data.
- **XY-serie / XY-spridningsdiagram** — Gnumeric's technical XY chart type and its Swedish compound form.
- **ytdiagram** — established Swedish chart type.
- **none / percent** — exact option values quoted from the Gnumeric error-category control; retained as displayed source values.

Batch 171:

- **Gnumeric** — application name; retained in branded compounds such as *Gnumeric-användare* and *Gnumeric-kalkylblad*.
- **A1- / R1C1-notation** — standard spreadsheet cell-reference notations; the letter-number identifiers are fixed technical terms.

Batch 172:

- **Gnumeric-inställningar** — Swedish compound containing the application name.
- **kalkylbladsflik / kalkylbladsflikens** — regular Swedish compounds for a worksheet tab and its possessive form.

Batch 173:

- **Shift** — exact keycap name in the help text; retained as the key label.

Batch 174:

- **Sheet1 / Sheet3** — literal worksheet names in the copy-and-paste example; preserved exactly.
- **Autospara / autosparandefunktionen** — Swedish UI term and its compound form for the AutoSave feature.
- **kalkylbladsflikarna / kalkylbladsflikens / textfärgsknappen** — regular Swedish compounds for the controls described in this passage.

Batch 176:

- **Gnumeric-gränssnittet** — Swedish compound with the application name.
- **ångrahistorik / ångrahistoriken** — Swedish terminology and inflection for the undo history feature.

Batch 177:

- **Gnumeric / gnumeric** — application name and command-line invocation.
- **.gnumeric / .gnum / .gnm** — file extensions named in the format documentation.
- **XML / Extensible Markup Language / gzip / OASIS Open Document Format for Office Applications / ODF / ECMA / IEC / Amd / 2nd Edition / ISO/IEC identifiers** — canonical names and identifiers of formats and standards.
- **LC_ALL / fr_FR / fr / FR / bash / ssconvert / Nautilus / rm** — environment variable, locale identifier, shell, applications and command-line tool names.
- The untranslated **LC_ALL=fr_FR gnumeric &** catalog entry is a command example containing no prose; it is intentionally identical to the source.

Batch 178:

- **.as / .db / .dif / .gnm / .gnumeric / .mps / .oleo / .pln / .psisheet / .px / .stc / .sxc / .wk1 / .wks / .xml** — file extensions in the format table.
- **Applix / GNU Oleo / Lotus 1-2-3 / MOOX / ODF / OpenDocument / OpenOffice.org / PlanPerfect / PostScript / SpreadsheetML / StarOffice** — product names and standardized file-format names.
- **application/* MIME strings / none** — exact MIME identifiers and a source table sentinel; preserved verbatim.
- **ECMA376 / ISO29500 / ISO/IEC** — standard identifiers preserved in the table.
- `l10n-lint` reported two dash warnings for **Lotus 1-2-3** and the matching `vnd.lotus-1-2-3` MIME string. Both hyphenated number sequences are part of the exact product or MIME identifiers and must remain unchanged.

Batch 179:

- **.gnumeric / .me / .slk / .sylk / .text / .txt / .wb1 / .wb2 / .wb3** — format extensions preserved verbatim.
- **Quattro Pro / SC / XSpread / SYLK / Xbase / OASIS and XML format names** — canonical file-format, standard and product labels.
- **Gnumeric-filformatet / Gnumeric-version** — valid compounds containing the product name.
- **application/*, x-*, vnd.*, dbase, dbf, zz-* / none** — MIME strings and the table's exact no-value sentinel; retained verbatim.
- **EXPERIMENTAL SAX based XML / SAX / based** — exact plugin label and XML parser terminology; preserved as named in the interface.

Batch 180:

- **.as / .dif / ASCII / XSD / CSV / TSV / JWorkbook / VisiCalc / Applix / Applixware / Gnumeric / Vistasource / Vim / Emacs / zcat / gunzip** — file extensions, formats, projects, products, editors, and command names.
- **Book1.gnumeric / Book1.text / Book1.text.gz** — literal filenames in the shell examples.
- **Gnumeric-kärnan / Applixware-kalkylprogrammet / Java-språket / CSV- / TSV-filer** — valid compounds or technical labels; Hunspell splits at markup and acronym boundaries.
- **Data Interchange Format / JWorkbook / XML** — canonical format and project names.

Batch 181:

- **2ε / TeX / LaTeX / longtable / pdflatex / Device Independent / DVI / PostScript / PDF** — language, processor, environment and output-format names.
- **ASCII-kodad / TeX-kommentarer / Oleo-projektet** — valid technical compounds containing fixed format/project names.
- **Book1.tex / Book1.pdf / HTML / Hypertext Markup Language / Markup / table** — literal example filenames, canonical language/format names, and the HTML `<table>` element.
- **GNU Oleo / VisiCalc / JWorkbook / Applixware / Mozilla** — product and project names preserved from the source.

Batch 182:

- **LaTeX / TeX / LaTeX-makron** — typesetting language and technical macro name.
- **\\usepackage, \\def, \\input, \\documentclass, \\begin, \\end, \\gnumeric* macros, longtable, lscape, UCS, inputenc, hhline, multirow, array, color, calc, ifthen** — literal code examples; preserved exactly.
- **MPS / .mps / ASCII-kodat / International Business Machines Corporation** — file format, extension, encoding and company name.
- **MIPLIB / Argonne National Laboratory / Bruce A. Murtagh / J. L. Nazareth / Murtagh / Nazareth** — project, institution and author names.
- **NAME / ROWS / COLUMNS / RHS / RANGES / BOUNDS / ENDATA / Field / Columns / type / bound / value / row / name / range** — MPS syntax and column labels in the verbatim template.
- **Lotus 1-2-3 / Lotus SmartSuite / SpreadsheetML / ZIP** — product and format names. `l10n-lint`'s two dash warnings for Lotus 1-2-3 are retained as required by the product name.
- `l10n-lint` also reports one repeated `RHS` and one numeric-range dash warning in the exact MPS syntax block; both are part of the required sample and remain unchanged.

Batch 183:

- **ODF / OpenDocument-format / ODF-kalkylblad / ODF-filer / SpreadsheetML / XML / SYLK / ZIP** — standardized formats, markup languages and file types.
- **OpenOffice.org / Microsoft Office / Microsoft Excel / Gnumeric / Multiplan / SmartSuite** — product names and branded compounds.
- **Open Specification Promise / ECMA / IEC / ISO/IEC** — exact standard and legal-program names.
- **Symbolic Link Interchange** — expansion of the SYLK format name.
- **.slk / none** — exact extension and table sentinel.

Batch 184:

- **Organization for the Advancement of Structured Information Standards (OASIS)** — official organization name kept verbatim.
- **MIME / ODF / IEC / ZIP / content.xml / mimetype / unzip** — MIME terminology, file names, standards and command name.
- **OpenOffice.org / Calc / LibreOffice Calc / PlanPerfect / StarCalc / StarOffice / Gnumeric** — product names and branded compounds.
- **PostScript / GGV / ghostview / gv / ghostscript / PDF** — format and program names; PostScript compounds are valid Swedish technical terms.

Batch 185:

- **.text / .txt / ASCII / TROFF / GROFF / SC / XSpread / Xspread / sc** — file extensions, encodings, commands and historical program names.
- **gPDF / Xpdf / GGV / ghostview / gv / ghostscript / Gnumeric / Corel / QuattroPro** — application and vendor names.
- **PostScript-språket** — valid Swedish technical compound with the format name.
- **none** — exact table sentinel retained from the source.

Batch 186:

- **Aston-Tate / Borland / Corel / FoxPro / dBase / XBase / Xbase / xBase / Visual FoxPro / SCO / W3C** — vendor, database and standards names.
- **TROFF / GROFF / groff / -me / -t / -Tps / -Tascii / PostScript / ASCII** — command names, options and output formats.
- **myfile.me / myfile.ps / myfile.ascii** — exact filenames in terminal examples.
- **January / February / March / April / May / June / July / August / September / October / November / December / Sheet / Operating System / DOS / Linux / Totals** — literal labels in the unchanged sample output table.
- **The dollar amounts and ASCII borders** are fixed sample output; the lint notice about currency localization is not applicable to this verbatim command output.
- **XHTML / HTML / XML / Extensible Markup Language / Hypertext Markup Language / Transitional / table** — standard names and literal HTML element identifier.

Batch 187:

- **ASCII / ISO-8859-1 / ISO-8859-x / UTF-8 / Unicode / GNU / Microsoft** — encoding and platform names kept as identifiers.
- **FAQ / Gnumeric** — abbreviation and application name.
- **glyf** — technical term for a glyph representation in a font.
- **Alphabet / Soup** — words in the proper title “The ISO-8859 Alphabet Soup”, preserved as part of the cited webpage title.
- **åÕÛÛÞ** — deliberately nonsensical example of mojibake from the source, preserved exactly.

Batch 188:

- **Ctrl- / Ctrl-F3 / F2 / F4 / Shift-Ctrl-G** — literal keyboard shortcut labels; preserved exactly.
- **Gnumeric** — application name.

Batch 189:

- **Gnumeric** — application name.
