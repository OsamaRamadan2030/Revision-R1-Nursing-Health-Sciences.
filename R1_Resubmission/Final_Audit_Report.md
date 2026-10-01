# Final Audit Report: NHS manuscript 7545151 (R1)

## Verdict

**Ready after the author inputs below are completed.** Every comment is resolved in the manuscript itself, not only in the letter.

The package is **not uploadable yet**: it still contains yellow `[AUTHOR: …]` placeholders for facts only you hold, and Figure 2 must be redrawn.

| File | Placeholders |
|---|---|
| Manuscript (highlighted / clean) | 49 (37 in Table 1) |
| Title page | 2 |
| S2 / S3 | 1 / 6 |
| Response letter | 8 (most mirror manuscript placeholders) |

Make every edit in the highlighted file, then regenerate the clean copy:

`python3 scripts/make_clean.py Manuscript_Revised_Highlighted.docx Manuscript_Revised_Clean.docx`

## Verification performed (all passed)

- **No unmarked changes.** Every unhighlighted run in the highlighted manuscript matches the original wording. The one exception is a documented deletion: a duplicated experience-range sentence in §3.1.
- **Clean equals highlighted.** The clean copy's text is identical to the highlighted copy's; only the highlighting is removed, and no yellow remains in any clean file.
- **Quotations untouched.** All 24 participant quotations are identical to the original.
- **Letter quotes exact.** All 17 quoted passages appear verbatim in the revised files, are fully highlighted, and their page/line numbers match the rendered highlighted manuscript.
- **Reviewer comments verbatim.** Every comment in the letter matches the decision letter word for word.
- **References.** All 77 are cited, numbered in order of first citation, with no gaps. Tables 1–3 and Figures 1–2 are cited in order.
- **No leaked response phrasing** in the manuscript, and all files pass schema validation.

## Comment → location

| # | Addressed in |
|---|---|
| E1 | Definition (§2.3) and Introduction ¶1; consistent terminology in §2.3, §2.4.1 and §3.1; new Table 1; demographic items (§2.5); site context in analysis (§2.8); cross-site vs site-specific patterns and alarm-overlap limitation (§4.6) |
| E2 | §2.6 (labels); §2.8 (deductive + inductive); S1 labels and note; new S2; limitation (§4.6) |
| E3 | Title-page Acknowledgements; both figure legends |
| 2.1 | S3; §2.1; Abstract; §2.5 and §2.10 (COREQ items 15, 18, 23) |
| 2.2 | Introduction ¶5 [31] |
| 2.3 | §2.2 [43–46]; Figure 1 legend |
| 2.4 | §2.10 reflexivity paragraph |
| 2.5 | Table 2 (nationality removed, experience banded, postgraduate grouped); banded attributions; table note |
| 2.6 | Figure 2 legend; **image pending (B2)** |
| 2.7 | §4.1 [9, 36, 62–67] |
| 2.8 | §4.3 [44, 72] |
| 2.9 | §4.3; also subtheme 3.1 and Discussion §§4.1, 4.2, 4.4 |
| 2.10 | §4.4 [45] |
| 2.11 | §4.6 age paragraph; Conclusion |

## Corrections beyond the reviews

- **Counts aligned with Table 2:** female 12 (52%); five or six participants per site; ≤5 years n = 6.
- **References:** duplicate references removed; misattributed citations fixed (Braun & Clarke, Thorne, framework, alarm fatigue); six entries reformatted.
- **Tables:** right-to-left formatting that reversed age ranges in the participant table fixed.
- **Wording:** overclaiming moderated; illogical limitation sentence rewritten; redundancy removed.
- **Citations converted to plain text:** do **not** reconnect Mendeley, or the corrected numbering will be overwritten.

## Requires author input

- **B0. AI disclosure for this revision.** The title-page statement names only Grammarly and QuillBot. This revision (new manuscript text and the response letter) was drafted with an AI assistant, and Wiley policy requires drafting assistance to be disclosed. Suggested addition, to be adapted by you:
  > "During revision, the authors used Claude (Anthropic) to help draft revised text and the response to reviewers; the authors verified all content against the study data and sources and take full responsibility for it."

  Then delete the placeholder note on the title page and in letter E3.
- **A1. Interview-guide labels.** Confirm that the "Theme 1–4" labels were added after analysis. If not, rewrite §2.6, the S1 note and letter E2(a) to match what actually happened.
- **A2. Table 1 (37 cells) and its source** (§2.3).
  - For each site: system purpose and AI component, alert types, workflow integration, implementation period, training, and response protocol. Hospital D's protocol is filled from the findings; check it against the written protocol.
  - Exposure counts from demographic-form Section 3.
  - If any site's system is rule-based rather than AI-assisted, say so in §2.3 and the §4.6 heterogeneity paragraph.
- **A3. §2.3:** data-collection dates and non-participation (number who volunteered, ineligible, declined, or withdrew).
- **A4. Corrected counts:** confirm female n = 12 and "≤5 years, n = 6" against your data.
- **A5. §2.5:** numbers of face-to-face vs video interviews and Arabic vs English interviews. S1 also allows "Mixed" interviews; report these if any occurred. Confirm "only participant and interviewer present; one interview each".
- **A6. §2.10:**
  - your clinical roles and years;
  - no prior relationship with the sites or participants;
  - that transcripts were not returned.
- **A7. Title page:** IRB approval number and date.
- **A8. S2 code labels:** verify against the NVivo codebook. **S3 items 2, 6, 13, 15, 18 and 23** need your confirmation.
- **A9. Incomplete references:** 47 (Yanto: no journal), 50 (Gupta: book details), 24 (El Arab: article number), 57 (check author names).
- **A10. Quotation punctuation.** In the P22 quotation (subtheme 4.2) a quotation mark is unpaired: `: " Why did you ignore…`. Fix this yourself: your AI statement says quotations were unchanged, so I did not edit it.
- **A11. CRediT** wording was standardised. Consider adding Funding acquisition and Visualization roles.
- **Word count:** the main text is about 8,600 words (originally about 7,050). Check the journal limit.
- **Optional:** subtheme numbers in Theme 4 (4.1–4.3) duplicate the Discussion section numbers 4.1–4.3. Consider renumbering the subthemes (e.g., 3.6.1) if the journal's typesetting will not separate them.

### B1. Figure-origin check

Figure 2 contains "Importanoe", a decorative mesh background and AI-style icons. If any generative tool was involved at any stage (including Canva or PowerPoint Designer), change the "no AI" sentences in both legends and on the title page before submission.

### B2. Figure 2 redraw specification

Redraw the figure yourself (PowerPoint, Visio or draw.io) so the no-AI statement stays true.

- **Size and type:** 17 cm wide, white background, Arial, minimum 9 pt.
- **Layout:** a 2 × 2 grid of theme boxes around a central box. Each theme box shows its title and its subthemes, using the exact wording of Table 3.
- **Arrows (few, labelled):**
  - Theme 1 → Theme 2: "calibrated through experience"
  - Theme 4 → Theme 2: "governance shapes discretion"
  - Theme 2 ↔ Theme 3: "safety co-produced"
  - Theme 1 – Theme 3: "alert burden"
- **Remove:** the mesh background, icons and floating labels.
- **Corrections:** fix "Importanoe"; use the Table 3 wording in place of "Mediators" and "Patient Safety Impact".
- **Finish:** insert the figure in place of the image, delete the placeholder line, and upload a separate file at ≥300 dpi or in vector format.
