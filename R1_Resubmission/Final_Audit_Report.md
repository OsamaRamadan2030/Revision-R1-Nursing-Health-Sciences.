# Final Audit Report: Between Alert and Action (NHS manuscript 7545151, R1)

## Verdict

**Ready after you resolve the items in "Requires author input".** The scientific and structural revision is complete, and every editor and reviewer comment is addressed in the manuscript. The package still contains **`[AUTHOR: …]` placeholders** for facts that only you hold (system characteristics, dates, interview counts, ethics number, interviewer background). Figure 2 also still has to be redrawn. **Do not upload until every placeholder has been replaced and the placeholder highlighting removed.**

| File | Placeholders to resolve |
|---|---|
| Manuscript_Revised_Highlighted.docx / _Clean.docx | 48 (37 of them in the new Table 1) |
| Title_Page_Revised (Highlighted / Clean) | 1 |
| S2_Supplementary_Analytic_Trail.docx | 1 |
| S3_COREQ_Checklist.docx | 6 |
| Response_to_Editor_and_Reviewers.docx | 7 (5 of them are quotations of manuscript placeholders, which update automatically once you fill the manuscript; 2 are notes to delete) |

Make every edit in the **Highlighted** file. Then either re-derive the clean copy (from the `R1_Resubmission` folder: `python3 scripts/make_clean.py Manuscript_Revised_Highlighted.docx Manuscript_Revised_Clean.docx`) or make the identical edit in the clean file, so that the two cannot drift apart.

---

## Comment-by-comment verification

| # | Concern | Where addressed (highlighted manuscript) | Verified |
|---|---|---|---|
| E1a | Define the AI component; distinguish it from conventional alarms and rule-based CDS | §2.3 new definition paragraph (pp. 6–7, ll. 171–183); Introduction ¶1 new sentence | ✔ |
| E1b | Purpose, alerts, and workflow integration per hospital (concise table, anonymised) | New **Table 1** (p. 7) | ✔ structure; **cells need your data** |
| E1c | Duration of implementation and participants' exposure from the demographic form | Table 1 rows 5 and 8–10; §2.5 demographic-form sentence; §3.1 cross-reference | ✔ structure; **cells need your data** |
| E1d | How site differences in technology, exposure, training, and protocols informed interpretation | §2.8 new paragraph "Site-level differences…" (p. 11, ll. 303–309) | ✔ |
| E1e | If the distinction cannot be made, explain and discuss the implications | §4.6 new paragraph "The four sites used different…" (p. 28, ll. 767–776) | ✔ |
| E2a | Were the "Theme 1–4" labels present during data collection? | §2.6 sentence; S1 labels replaced and explanatory note added | ✔ **you must confirm the fact (see A1)** |
| E2b | Relationship among framework, questions, codes, and themes | §2.8 new paragraph (p. 11, ll. 286–302); new **Supplementary File S2** | ✔ **verify code labels (A6)** |
| E2c | Deductive, inductive, or both? | §2.8 ("combined deductive and inductive elements"); §2.2 closing sentence | ✔ |
| E3 | AI-use disclosure | Title page Acknowledgements (your exact statement) plus figure statement; Figure 1 and 2 legends | ✔ see note B1 |
| R1 | Positive; no requests | No change needed | ✔ |
| 2.1 | COREQ checklist | New **Supplementary File S3**; §2.1; Abstract (Design) | ✔ |
| 2.2 | Explain Vision 2030 | Introduction ¶5 (p. 3, ll. 89–93), new reference [31] | ✔ |
| 2.3 | Underpinning reference for Figure 1; AI disclosure | §2.2 (p. 5, ll. 140–148), refs [43–46]; Figure 1 legend | ✔ |
| 2.4 | Interviewer's relationship to the settings; ICU background | §2.10 new reflexivity paragraph (p. 13, ll. 351–361) | ✔ **2 placeholders** |
| 2.5 | Confidentiality in Table 1 | Nationality removed; experience banded; MSN/PhD combined; attributions banded; table note | ✔ |
| 2.6 | Figure 2 illegible | Legend revised; **image must be redrawn by you** (spec below) | ✖ **pending** |
| 2.7 | References for former ll. 569–575 | §4.1 rewritten with refs [9, 36, 62–67] | ✔ |
| 2.8 | Reference for "sociotechnical perspectives" | §4.3, refs [44, 72] | ✔ |
| 2.9 | Former l. 608: "This suggests" | §4.3, now "These findings suggest…" | ✔ |
| 2.10 | Former l. 621: "This suggests" | §4.4, now "Taken together, these accounts suggest…" | ✔ |
| 2.11 | Age range 26–51 | §4.6 new paragraph (p. 28, ll. 777–791); Conclusion | ✔ |

All 25 quotations in the response letter were extracted by script from the revised files. Each one was checked and matches the manuscript, title page, or S1 character for character. The text of the highlighted and clean manuscripts is identical; only the formatting differs.

---

## Major issues found and fixed (not raised by reviewers)

1. **Participant numbers contradicted Table 1.** The text said 13 female participants (57%), but Table 1 lists 12 (52%). The text said five to seven participants per site, but the table shows 5, 6, 6, and 6. The text said nurses with fewer than five years' experience numbered 7, but the table gives 5 (<5 years) or 6 (≤5 years). All three were corrected to match Table 1, which agrees with every quotation attribution. **Please confirm A4.**
2. **Duplicate references.** Ref 35 duplicated ref 12 (Almagharbeh), and ref 36 duplicated ref 26 (Hassanein). Both were merged.
3. **Mis-cited sources.**
   - "Braun and Clarke (2022) [39]" pointed to Byrne (2022). The Braun & Clarke book is now cited.
   - The framework sentence cited a knowledge-graph education study (Liu et al.). This was removed and replaced with the framework sources.
   - Interpretive sufficiency was cited to an AI-adoption review. It now cites Thorne; the review was moved to the Introduction, where it fits.
   - The alarm-fatigue statement cited a review protocol and a health-students review. These now cite alarm-fatigue sources, and both original papers were re-placed where they fit (technology acceptance; education).
   - The sentence on negotiation as judgment cited an alarm-management study. It now cites Tanner.
4. **Mendeley field codes** were converted to static text. If anyone refreshes Mendeley in this file, the corrected numbering would be overwritten. **Do not reconnect Mendeley to these files.**
5. **Right-to-left table text.** The template's Normal style is RTL (Arabic), so participant-table cells displayed age ranges reversed ("40–36"). This affected the original submission too. All table cells are now explicitly left-to-right.
6. **Theme structure mirrors the interview guide.** This is the issue behind Editor comment E2: every theme, and most subthemes, map one-to-one onto guide sections B1–B4. The revision does not deny this. Instead it (a) explains that the correspondence follows from the areas of inquiry, (b) names the interpretations that were not predefined, (c) adds an analytic trail (S2), and (d) lists the correspondence as a limitation. This is the defensible position; claiming the themes were wholly emergent would not survive scrutiny.
7. **Overclaiming in a qualitative design** was moderated:
   - Abstract conclusion: "requires" → "findings suggest … depends on"
   - Key point 3: → "is likely to depend on"
   - §4.2: governance "is as important as" → "may be as important as"
   - §4.4: implementation strategy "is a major influence" → "may be"

## Minor issues and wording improvements

- Introduction: "has only limitedly examined" was rewritten. Missing commas around the relative clause in ¶1 were added.
- §2.1: a stray comma before "to explore" was removed.
- §4.6: "Purposive recruitment may also have favoured…" was illogical and has been rewritten.
- "dual-analyst coding" overstated a 3-transcript check. It now reads "independent coding of a subset of transcripts by a second analyst".
- All ambiguous "This suggests / This highlights / This adds" sentences were rewritten (subtheme 3.1; §§4.1–4.4).
- "Supplementary File 1" was standardised to "Supplementary File S1".
- Reference formatting fixes: refs 18 ("Volume 18"), 42 (DOI junk), 53 (Cope: journal restored), 57 (duplicated title), 60 (DOI suffix), and 71 (`<scp>` tags).
- Title page: the trailing full stop was removed from the title. CRediT entries were corrected: the duplicated "Writing – review & editing" was removed, and the non-CRediT terms "support" and "Data interpretation" were replaced with CRediT degree labels.

## Inconsistencies found between files

- S1 labelled its sections "Theme 1–4", which conflicted with an inductive analysis. Fixed (see A1).
- The title page and manuscript titles differed by a trailing full stop. Fixed.
- **Ethics approval number** was missing from both the title page and the manuscript. A placeholder was added to the title page; the blinded manuscript says the number is withheld for review.

## Methodological notes

- The **COREQ** checklist (S3) uses section numbers rather than page numbers. Six items need your confirmation.
- **Word count:** the main text (Introduction–Conclusion, excluding tables and references, but including quotations, legends, and table notes) is about **8,700 words**, up from about 7,050. The abstract is 217 words. Almost all additions were requested. **Check the current Nursing & Health Sciences limit** (the author guidelines could not be retrieved from this environment). If you need to trim, the safest cuts are the duplicated framework description in the Figure 1 legend and the first two sentences of §4.5.
- Reference style is Vancouver numeric, as in the original. The editor did not query it.

---

## Requires author input

Each item gives the exact location and the wording to use.

**A1. Confirm that the "Theme" labels were added after analysis** (Editor E2a). The letter, §2.6, and the S1 note all say this. If it is **not** true (that is, the labels existed during interviews), replace the §2.6 sentence with:
> "Section headings in the guide used provisional labels derived from the framework; these were treated as topic areas, not as themes, and the final themes were developed through analysis (Section 2.8)."

Also adjust the S1 note and response E2(a) to match.

**A2. Table 1 (37 cells) and the §2.3 source sentence.** Supply, for each hospital:
- system purpose and AI component (e.g., "machine-learning sepsis risk score updated every 15 min from vitals, laboratory results and nursing documentation")
- principal alert types
- workflow integration (central monitor / EHR banner / mobile device)
- time since implementation
- training at implementation
- response protocol (Hospital D's protocol is filled from the findings; confirm it against the written protocol)

Exposure rows come from demographic-form Section 3 (duration-of-use categories, formal training, prior experience).

**If any site's system turns out to be rule-based** (e.g., an electronic NEWS calculator) rather than AI-assisted, replace the second sentence of the §2.3 definition paragraph with:
> "At [Hospital X], the system combined a rule-based aggregate score with [describe]; we retained these participants because their accounts concerned automated deterioration alerting, and we note this heterogeneity in Section 4.6."

**A3. §2.3:** add the data collection period and non-participation. For example:
> "Of the 27 nurses who contacted the research team, 25 met the eligibility criteria; two were not interviewed because of extended leave."

**A4. Confirm the corrected counts:** female n = 12 (52%); "five or fewer years … (n = 6)" in subtheme 2.1. If your analysis memo shows a different subgroup, use those figures, but they must agree with Table 2.

**A5. §2.5:** add the number of face-to-face and video interviews, and of Arabic and English interviews.

**A6. S2 code labels** are illustrative labels derived from the reported findings. Check them against your NVivo codebook and replace them with your actual code names.

**A7. §2.10 interviewer paragraph:**
- your clinical roles and years of practice, e.g., "who worked as an adult ICU staff nurse for 6 years and a paediatric critical care nurse for 4 years before entering academia"
- confirmation that you had no prior relationship with the four hospitals or with any participant

**A8. Title page:** the IRB approval number and date.

**A9. S3 items:** 2 (your degree), 6, 13, 15, 18, and 23.

**A10. CRediT:**
- Confirm the reworded roles.
- Consider whether **Funding acquisition** should be listed. The grant is from Najran University, which is the affiliation of author 2.
- Consider whether **Visualization** (the figures) should be listed, and for whom.

**A11. Incomplete references:** please complete these from the source:
- ref 47 (Yanto et al., 2025): no journal or DOI
- ref 50 (Gupta, "Codes and Coding"): book title, editors, and publisher missing
- ref 24 (El Arab et al.): "7 September:1–17" should be the article number
- ref 57: check the author names ("Ul Z, Kakar H")

**A12. Verify the content of moved or added citations.** Each was placed on the strength of its title and abstract:
- [4, 5] AI vs rule-based alerting
- [12] in the Introduction
- [63] technology acceptance
- [76] education

### B1. AI disclosure for the figures: please read

Your instruction was that no AI was used to create the figures, and the title page and both legends now say so. However, Figure 2 has several features that editors increasingly associate with generative image tools:
- the misspelling **"Importanoe"** inside the "Human layer of safety" box
- a decorative node-and-line background mesh
- AI-style icon sets

If a designer, a template service, or any tool with built-in generative AI (for example, Canva's Magic features, PowerPoint Designer/Copilot, ChatGPT/Gemini image generation, or BioRender AI) was involved at any stage, the statement must be changed before submission. An inaccurate disclosure is far more damaging than an accurate one. If any tool was used, replace the legend sentence with:
> "Figure [n] was drafted by the authors and rendered using [tool]; all content was specified and verified by the authors."

Mirror that change in the title-page sentence.

### B2. Figure 2 redraw specification (Reviewer 2.6)

Redraw the figure yourself in PowerPoint, Visio, or draw.io. This keeps the "no AI" statement true. Then insert it in place of the current image (delete the highlighted placeholder line above the legend) and upload it separately at 300 dpi or more (TIFF or PNG) or as a vector PDF/EPS.

- **Canvas:** 17 cm wide (full page width), white background, no mesh, no icons.
- **Fonts:** Arial or Helvetica, minimum 9 pt at final size. Theme titles 11 pt bold; subthemes 9–10 pt.
- **Layout:** a 2 × 2 grid of four rounded rectangles (one per theme) around a central box reading "Critical care nurses' experiences of AI-assisted early warning (Saudi adult ICUs)".
- **Box contents:** each theme box contains its title, followed by its 2–3 subtheme labels as a bulleted list. Remove the separate subtheme callouts.
- **Labels:** use the exact wording of Table 3, for example "Theme 1. Learning to read the machine": 1.1 First encounters and orientation; 1.2 Developing a working relationship with the algorithm; 1.3 Navigating alert volume and frequency (and likewise for Themes 2–4).
- **Arrows:** use a few labelled arrows that reflect interpretations stated in the text:
  - Theme 1 → Theme 2: "calibrated through experience"
  - Theme 4 → Theme 2: "governance shapes discretion"
  - Theme 2 ↔ Theme 3: "safety co-produced at the bedside"
  - Theme 1/3 link: "alert burden"
- **Colour:** one muted fill per theme, colour-blind safe. Black text throughout.
- **Corrections:** fix "Importanoe" → "Importance". Replace "Patient Safety Impact" and "Mediators" in the old legend with the Table 3 wording.
- **Remove:** the floating labels ("Multinational workforce", "Varied experience (2–23 years)", "Different hospital sites", "Clinical Judgment & Patient Safety are Emergent from Context"). They are not findings and add clutter.
