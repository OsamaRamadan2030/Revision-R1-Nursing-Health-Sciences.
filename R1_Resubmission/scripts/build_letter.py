import re, sys
sys.path.insert(0, '/tmp/rt2')
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from locate import loc

MS = docx.Document('Manuscript_Revised_Clean.docx')
MS_PARAS = []
for p in MS.element.body.iter(qn('w:p')):
    MS_PARAS.append(''.join(t.text or '' for t in p.iter(qn('w:t'))))
TP = docx.Document('Title_Page_Revised_Clean.docx')
TP_PARAS = [p.text for p in TP.paragraphs]
S1 = docx.Document('S1_Supplementary_Interview_Guide_Revised_Clean.docx')
S1_PARAS = [''.join(t.text or '' for t in p.iter(qn('w:t'))) for p in S1.element.body.iter(qn('w:p'))]

USED = []
def Q(start, end=None, src='ms'):
    """Exact substring of the revised file from start..end (inclusive)."""
    paras = {'ms': MS_PARAS, 'tp': TP_PARAS, 's1': S1_PARAS}[src]
    for t in paras:
        i = t.find(start)
        if i >= 0:
            if end is None:
                return t[i:].rstrip()
            j = t.find(end, i)
            assert j >= 0, ('end not found', end)
            s = t[i:j + len(end)]
            USED.append(s)
            return s
    raise AssertionError('quote start not found: ' + start)

def L(start, end=None):
    r = loc(start, end)
    assert r, ('locate failed', start)
    return r

doc = docx.Document()
st = doc.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(2.54); s.left_margin = s.right_margin = Cm(2.54)

def shade(p, fill):
    pPr = p._p.get_or_add_pPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill); pPr.append(shd)

def border_left(p, color='1F3864'):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr'); l = OxmlElement('w:left')
    for k, v in (('val', 'single'), ('sz', '18'), ('space', '8'), ('color', color)): l.set(qn('w:' + k), v)
    b.append(l); pPr.append(b)

PH = re.compile(r'(\[AUTHOR:[^\]]*\])')
def runs(p, text, bold=False, italic=False, size=None, color=None):
    for part in PH.split(text):
        if not part: continue
        r = p.add_run(part); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor.from_string(color)
        if PH.fullmatch(part):
            r.font.highlight_color = 7  # yellow
    return p

def para(text='', bold=False, italic=False, align=None, size=None, after=None, color=None):
    p = doc.add_paragraph(); runs(p, text, bold, italic, size, color)
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    return p

def heading(text):
    p = para(text, bold=True, size=13, color='1F3864', after=6)
    p.paragraph_format.space_before = Pt(14)
    pPr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    for k, v in (('val', 'single'), ('sz', '6'), ('space', '1'), ('color', '1F3864')): bt.set(qn('w:' + k), v)
    b.append(bt); pPr.append(b)

def comment(label, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
    runs(p, label + ' ', bold=True, color='1F3864'); runs(p, text, italic=True)
    shade(p, 'EEF3FA')

def response(text):
    p = doc.add_paragraph(); runs(p, 'Response: ', bold=True); runs(p, text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def revised(where, text):
    p = doc.add_paragraph(); runs(p, f'Revised text ({where}):', bold=True, italic=True, size=11)
    p.paragraph_format.space_after = Pt(2)
    q = doc.add_paragraph(); runs(q, '“' + text + '”', size=11)
    q.paragraph_format.left_indent = Cm(0.8); border_left(q); q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def bullet(text):
    p = doc.add_paragraph(style='List Bullet'); runs(p, text); p.paragraph_format.space_after = Pt(3)

# ---------------------------------------------------------------- header
box = para('BEFORE SUBMISSION — delete this box. This letter quotes the revised manuscript exactly, including the bracketed [AUTHOR: …] placeholders that mark information only the authors hold (system characteristics, dates, interview counts, ethics approval number, interviewer background). Every placeholder must be completed in the manuscript, the title page, Supplementary Files S2–S3 and this letter, and the redrawn Figure 2 inserted, before the package is uploaded. The full list is in Final_Audit_Report.md.', bold=True, size=10)
shade(box, 'FFF2CC')
para('Response to the Editor and Reviewers', bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, after=10, color='1F3864')
for k, v in (('Manuscript ID', '7545151'),
             ('Title', 'Between Alert and Action: Nurses’ Experiences of AI-Assisted Early Warning, Clinical Judgment, and Patient Safety in Critical Care'),
             ('Journal', 'Nursing & Health Sciences'),
             ('Decision', 'Minor revision')):
    p = doc.add_paragraph(); runs(p, k + ': ', bold=True); runs(p, v); p.paragraph_format.space_after = Pt(0)
para('')
para('Dear Editor,')
para('Thank you for the opportunity to revise our manuscript, and thank you to both reviewers for their careful and generous reading. The comments have strengthened the paper, particularly in characterising the technology participants used and in making the analytic route from framework to themes transparent. We have addressed every comment individually below. Each response quotes the revised wording and gives its location. All changes are highlighted in yellow in the revised manuscript, and a clean copy is also supplied.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
para('We also reviewed the whole manuscript for internal consistency, and made the following corrections in addition to the points raised. None of them alters any finding or conclusion:', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
for b in [
    'Three transcription errors in the participant description were corrected against the participant data: the number of female participants (now n = 12, 52%; previously reported as 13, 57%), the number of participants per site (five or six; previously “five to seven”), and the number of nurses with limited critical care experience in subtheme 2.1 (now “five or fewer years … (n = 6)”).',
    'The reference list was corrected. Two duplicated entries were merged (former references 35 and 36 duplicated references 12 and 26). Several citations that did not support the sentence they were attached to were replaced. Braun and Clarke’s guide is now cited where their approach is named, Thorne is cited for interpretive sufficiency, and alarm-fatigue sources are cited for alarm-fatigue statements. One reference that did not relate to its sentence was removed. Formatting errors in six entries were corrected. Eleven new references were added in response to the comments, and the list was renumbered in order of first citation (77 references).',
    'A new Table 1 (AI-assisted systems and exposure by site) has been added. The former Tables 1 and 2 are now Tables 2 and 3.',
    'In the participant table, cell text direction was corrected. Under the template’s right-to-left default, age ranges such as 36–40 were displaying in reverse.',
    'Causal or overstated wording was moderated in the abstract conclusion, the key points, and the Discussion, in keeping with a qualitative design. The limitation on voluntary participation was rewritten so that it follows logically. The citation fields were converted to plain text so that the numbering cannot be overwritten by reference-manager software.',
    'Quotation attributions now report critical care experience in bands rather than exact years, as part of the confidentiality changes described under Comment 2.5. The wording of participants’ quotations is unchanged.',
]:
    bullet(b)
para('Page and line numbers in this letter refer to the highlighted revised manuscript. They may shift by a line or two depending on the software used to open the file.', italic=True, size=11)
para('We hope that the revised manuscript is now suitable for publication in Nursing & Health Sciences.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
para('Yours sincerely,', after=0)
para('Osama Mohamed Elsayed Ramadan, on behalf of all authors', after=0)
para('Corresponding author')

# ---------------------------------------------------------------- Editor
heading('COMMENTS FROM THE EDITOR')
comment('Comment E1.', 'Characterization of the systems and participants’ exposure. If possible, describe the systems used at each hospital, including their purpose, the component that qualifies them as AI-assisted, the alerts generated, and their integration into nursing workflows. Distinguish these systems from conventional monitoring alarms or rule-based decision-support systems. Please also report how long the systems had been implemented and participants’ experience using them, drawing on the information collected through the demographic form. Explain how differences in technology, exposure, training, and response protocols across hospitals informed the interpretation of the findings. A concise table may help present this information while preserving institutional anonymity. If this distinction cannot be made, please explain why and discuss the implications for interpreting the findings in the Discussion section.')
response('We agree that readers need to know what technology participants actually experienced. We have addressed each element of this comment as follows.')
p = para('(a) Definition and distinction from conventional alarms and rule-based systems.', bold=True)
response('We added an explicit working definition of AI-assisted early warning to the Methods. It distinguishes AI-assisted systems from single-parameter monitor alarms and from rule-based aggregate scores with fixed thresholds. The same distinction is now introduced briefly in the first paragraph of the Introduction.')
revised(f'Methods, Section 2.3, {L("For this study, AI-assisted early warning", "institutional anonymity.")}', Q('For this study, AI-assisted early warning', 'institutional anonymity.'))
revised(f'Introduction, paragraph 1, {L("Unlike conventional single-parameter", "risk estimates [4, 5].")}', Q('Unlike conventional single-parameter', 'risk estimates [4, 5].'))
para('(b) Purpose, AI component, alert types, workflow integration, duration of implementation, and response protocols at each site (concise table).', bold=True)
response('We added a new Table 1, “Characteristics of AI-Assisted Early Warning Systems and Participants’ Exposure, by Hospital Site”. For each hospital it reports the purpose and AI component of the system, the principal alert types, integration into nursing workflow, time since implementation, training at implementation, and the local response protocol. Vendor and product names are withheld to preserve institutional anonymity, as the editor suggested. [AUTHOR: the site-level cells of Table 1 are marked for completion from hospital informatics records and must be filled before submission; please delete this sentence once done.]')
para('(c) Participants’ exposure, drawn from the demographic form.', bold=True)
response('Table 1 now also reports, by site, participants’ duration of use of the system, formal training received, and prior experience with similar systems. These are the items collected in Section 3 of the demographic form (Supplementary File S1). The description of the demographic form in the Methods now lists these items, and the Findings refer readers to Table 1.')
revised(f'Methods, Section 2.5, {L("Before each interview, participants completed", "(Supplementary File S1).")}', Q('Before each interview, participants completed', '(Supplementary File S1).'))
revised(f'Findings, Section 3.1, {L("Participant characteristics are presented in Table 2", "by site in Table 1.")}', Q('Participant characteristics are presented in Table 2', 'by site in Table 1.'))
para('(d) How differences across hospitals informed interpretation.', bold=True)
response('We added a paragraph to the Data analysis section. It explains that site-level differences were treated as interpretive context rather than as variables for comparison, and describes how site-tagged coding and analytic memos were used. It also gives the two clearest examples from the findings.')
revised(f'Methods, Section 2.8, {L("Site-level differences in system type", "at Hospital A.")}', Q('Site-level differences in system type', 'at Hospital A.'))
para('(e) Implications for interpretation (Discussion).', bold=True)
response('Because the sites used different systems, and because AI-generated alerts were encountered alongside conventional monitor alarms, we added a paragraph to the Strengths and Limitations. It sets out what the findings can and cannot claim. The findings describe nurses’ experiences of AI-assisted early warning as implemented locally, not the performance of any single algorithm. Accounts of alert burden in particular may reflect the cumulative alerting environment.')
revised(f'Discussion, Section 4.6, {L("The four sites used different AI-assisted", "distinguish these sources.")}', Q('The four sites used different AI-assisted', 'distinguish these sources.'))

comment('Comment E2.', 'Transparency in theme development. The supplementary interview guide labels its sections “Themes 1–4,” closely corresponding to the final themes. Please clarify whether these labels were present during data collection or added retrospectively for presentation. Explain the relationship between the orienting conceptual framework, interview questions, initial codes, and final themes, distinguishing predefined areas of inquiry from interpretations developed through analysis. Please also clarify whether the analysis was deductive, inductive, or a combination of both.')
para('(a) Whether the “Theme” labels were present during data collection.', bold=True)
response('The theme labels were not present during data collection. During interviews, the guide sections were organised and labelled by area of inquiry, and each area corresponds to one study objective. When we prepared the supplementary file for submission, after analysis was complete, we added cross-references to the final themes for presentation. We now see that this wrongly implied the themes were predefined. We have replaced the cross-references with the area-of-inquiry labels used during data collection and added an explanatory note to Supplementary File S1. The Methods now state this explicitly.')
revised(f'Methods, Section 2.6, {L("These topics were organised into four areas", "(Section 2.8).")}', Q('These topics were organised into four areas', '(Section 2.8).'))
revised('Supplementary File S1, Part B, note before the Opening Statement', Q('During data collection, Sections B1–B4', 'and final themes relate.', src='s1'))
para('(b) Relationship between framework, interview questions, initial codes, and final themes; (c) deductive, inductive, or both.', bold=True)
response('The analysis combined both approaches. The orienting framework shaped the areas of inquiry, and therefore what participants were asked about. Codes and themes, however, were generated inductively, and no codebook was applied. We have added a paragraph to the Data analysis section that sets out this relationship. It acknowledges openly that the final themes broadly correspond to the areas of inquiry, and it names the interpretations that were not anticipated by the framework or the interview questions. A new Supplementary File S2 traces, for each theme, the predefined framework concepts and area of inquiry, illustrative initial codes, and the interpretation developed through analysis. We have also added the correspondence between the guide structure and the themes to the Limitations, so that readers can weigh it.')
revised(f'Methods, Section 2.8, {L("The analysis combined deductive and inductive", "final interpretation.")}', Q('The analysis combined deductive and inductive', 'final interpretation.'))
revised(f'Methods, Section 2.2, {L("It defined the broad areas of inquiry", "(Section 2.8).")}', Q('It defined the broad areas of inquiry', '(Section 2.8).'))
revised(f'Discussion, Section 4.6, {L("Finally, the four themes broadly correspond", "invited to discuss.")}', Q('Finally, the four themes broadly correspond', 'invited to discuss.'))

comment('Comment E3.', 'Disclosure of AI use. Please specify whether AI tools were used in preparing the manuscript. If they were used for drafting, language editing, grammar correction, or similar purposes, this information must be included in the Acknowledgements section on the title page. If AI tools were used to create or enhance Figures 1 and 2, this information must also be disclosed in the respective figure legends.')
response('AI tools were not used in the design or conduct of the study, in data analysis or interpretation, or to create or enhance either figure. The authors used Grammarly and QuillBot for grammar, spelling, and readability edits only. We have added the following statement to the Acknowledgements on the title page.')
revised('Title page, Acknowledgements', Q('The authors used Grammarly and QuillBot', 'full responsibility for its content.', src='tp'))
response('For transparency, both figure legends now also state that no AI tools were used to create or enhance the figure, and the title page states the same.')
revised(f'Figure 1 legend, {L("The figure was created by the authors; no artificial", "enhancement.")}', Q('The figure was created by the authors; no artificial', 'enhancement.'))

comment('Comment E4.', 'These revisions are essential to establish what technology participants experienced and how the analysis generated its interpretive contribution. Please submit a revised manuscript with a point-by-point response explaining how each concern has been addressed.')
response('Thank you. The technology is now characterised in the new Table 1 and Section 2.3 (Comment E1). The analytic route from framework to themes is set out in Section 2.8 and Supplementary File S2 (Comment E2). This letter provides the point-by-point response.')

comment('Handling editor.', 'The peer reviewers have recommended several additional minor revisions to your manuscript. Please address these comments and submit a revised manuscript accompanied by a detailed point-by-point response outlining how each reviewer comment has been addressed.')
response('All reviewer comments are addressed individually below.')

# ---------------------------------------------------------------- Reviewer 1
heading('REVIEWER 1')
comment('Comment 1.1.', 'The manuscript submitted by the authors is very well presented and comprehensively addresses the core aspects of research. The study is ethically sound, scientifically rigorous, and methodologically robust, with clear and technically accurate reporting of the methods and results. The scope of the manuscript is highly relevant to clinical practice, education, and future decision-making. The findings are presented in a balanced manner, offering a comprehensive understanding of participants’ perspectives. Importantly, the authors have also appropriately acknowledged and discussed the limitations of the study, reflecting transparency and critical reflection in reporting the research. Furthermore, the detailed presentation of the study has the potential to encourage similar research in other contexts and settings. Overall, the manuscript is reader-friendly, engaging, and contributes meaningfully to the existing body of knowledge.')
response('We thank Reviewer 1 for this positive assessment. No changes were requested. We have kept the strengths the reviewer identified, especially the balanced presentation of findings and the transparent treatment of limitations, while making the revisions requested by the editor and Reviewer 2. In line with the reviewer’s remark on transparency, the Limitations now also address the heterogeneity of the systems across sites, the age profile of the sample, the interviewer’s position, and the correspondence between the interview guide and the theme structure.')

# ---------------------------------------------------------------- Reviewer 2
heading('REVIEWER 2')
comment('General comment.', 'Thank you to the authors for this well-presented manuscript which presents research that highlights the complexity of integrating clinical judgement with technology use in critical care environments. The study is rigorous and adheres well to the chosen methodology. … The findings are informative and elucidate the necessity for critical thinking and following intuitive and experiential judgments alongside adapting to the technology. Reporting on contextual differences is an added strength of the multi-site study. I have provided some feedback for consideration, mainly relating to clarifying phrasing and supporting references. I also have a concern about table 1 and potential identification of participants. Please see below for more details.')
response('We are grateful for these comments. Following the editor’s request, we have strengthened the reporting of contextual differences across sites (new Table 1 and Section 2.8).')

comment('Comment 2.1.', 'Please consider adding a COREQ checklist to the submission to support reporting quality.')
response('We added the completed 32-item COREQ checklist as Supplementary File S3. For each item it gives the manuscript section where the item is reported, using section numbers rather than page numbers, which will change at typesetting. The Methods and the Abstract now refer to it.')
revised(f'Methods, Section 2.1, {L("Reporting followed the Consolidated Criteria", "Supplementary File S3.")}', Q('Reporting followed the Consolidated Criteria', 'Supplementary File S3.'))

comment('Comment 2.2.', 'Line 82, page 5 - An additional sentence to outline what Vision 2030 is would provide more context to this statement.')
response('We added a sentence explaining what Vision 2030 is, with reference to its Health Sector Transformation Program, before the statement about digital health priorities.')
revised(f'Introduction, paragraph 5, {L("Vision 2030, launched in 2016", "digital services [31].")}', Q('Vision 2030, launched in 2016', 'digital services [31].'))

comment('Comment 2.3.', 'Is there any underpinning reference for figure 1? If AI was used to develop the figure, please disclose this or add in any supporting references used.')
response('The framework in Figure 1 was developed by the authors. We now state the three bodies of work that underpin it, with references: Tanner’s clinical judgment model [43], Sittig and Singh’s sociotechnical model of health information technology [44], and the literature on trust in automation and alarm fatigue [11, 45, 46]. The legend repeats these sources and states that no AI tools were used to create or enhance the figure (see also Comment E3). We also removed a citation from this paragraph that did not relate to the framework.')
revised(f'Methods, Section 2.2, {L("The framework was developed by the authors from", "contextual influences.")}', Q('The framework was developed by the authors from', 'contextual influences.'))
revised(f'Figure 1 legend, {L("Figure 1. Orienting", "enhancement.")}', Q('The framework was developed by the authors as a non-causal', 'enhancement.'))

comment('Comment 2.4.', 'Did the researcher/ interviewer have any relationship with any of the settings? For example, have they previously worked in ICU? Please consider adding this information to the reflexivity statements on page 11; section 2.10.')
response('We added a reflexivity paragraph to Section 2.10. It describes the interviewer’s clinical background, his relationship (or lack of one) with the study settings and participants, and how his insider familiarity with critical care was managed during data generation.')
revised(f'Methods, Section 2.10, {L("The principal investigator is a male", "team meetings.")}', Q('The principal investigator is a male', 'team meetings.'))

comment('Comment 2.5.', 'I have some concerns that the confidentiality of the participants may be at risk though the information in table 1. For example, if there is only one male, Filipino ICU nurse working in hospital site A they would be able to be identified. I think the nationalities could be removed from this table, but the aggregated text could stay in (line 288, page 12).')
response('We agree, and thank the reviewer for this important point. We removed the nationality column from the participant table (now Table 2) and kept nationality only in the aggregated text, as suggested. Because combinations of the remaining characteristics could still single out individuals within a site, we took two further steps. Critical care experience is now shown in bands (≤5, 6–10, 11–15, >15 years). The single doctoral qualification is combined with master’s degrees as “Postgraduate”. Quotation attributions now use the same experience bands, so that quotations cannot be linked to an exact length of service. A table note explains these steps.')
revised(f'Findings, Table 2 note, {L("Note: To protect participant confidentiality", "doctoral degree (n = 1).")}', Q('Note: To protect participant confidentiality', 'doctoral degree (n = 1).'))

comment('Comment 2.6.', 'Figure 2 is very difficult to read. I appreciate the interconnectedness of all the concepts but please revise the figure to ensure all text boxes are easier to read.')
response('We agree. We redrew Figure 2 for legibility. The decorative background network was removed, all text is set at a minimum of 9 pt at final print width, and theme and subtheme labels now match Table 3 exactly. Each theme is shown with its subthemes in a single uncluttered block, and lines between themes are reserved for the interpretive relationships described in the text. We also corrected a typographical error in a subtheme box. The legend now explains that the connecting lines indicate interpretive relationships rather than causal pathways, and that no AI tools were used. [AUTHOR: insert the redrawn figure in the manuscript and upload it as a separate high-resolution file before submission; delete this sentence once done.]')
revised(f'Figure 2 legend, {L("Themes are shown with their subthemes", "enhancement.")}', Q('Themes are shown with their subthemes', 'enhancement.'))

comment('Comment 2.7.', 'Lines 569-571 page 22; please provide a reference to the earlier work mentioned here. Also, the statements on lines 572 -575 would benefit from additional referencing support.')
response('We rewrote this passage to name the earlier work and to support each statement. The “earlier work” is the body of technology-acceptance research that measures acceptance as an attitude or intention at adoption [9, 36, 62, 63], which our findings extend; the process view is supported by Greenhalgh et al.’s NASSS framework [64]. The statements on the Saudi context and on peer-mediated learning (former lines 572–575) are now supported by evidence on the Saudi nursing workforce and on the cultural adjustment of internationally recruited nurses [65, 66], and by Benner’s account of experiential learning [67].')
revised(f'Discussion, Section 4.1, {L("Earlier work has largely conceptualised", "need for structured onboarding.")}', Q('Earlier work has largely conceptualised', 'need for structured onboarding.'))

comment('Comment 2.8.', 'Line 604 -please provide a reference for ‘sociotechnical perspectives.’')
response('We added references to Sittig and Singh’s sociotechnical model [44] and to an empirical sociotechnical study of AI-enabled clinical decision support [72].')
revised(f'Discussion, Section 4.3, {L("This interpretation aligns with sociotechnical", "[44, 72].")}', Q('This interpretation aligns with sociotechnical', '[44, 72].'))

comment('Comment 2.9.', 'Line 608 – For clarity, rather than starting the sentence with ‘This suggests…’, consider rephrasing to, “These findings suggest…’')
response('We made the change as suggested. We also checked the whole manuscript for other sentences opening with an ambiguous “This suggests” or “This highlights” and revised them. These are in subtheme 3.1 and Sections 4.1, 4.2, and 4.4.')
revised(f'Discussion, Section 4.3, {L("These findings suggest that the safety", "most vulnerable.")}', Q('These findings suggest that the safety', 'most vulnerable.'))

comment('Comment 2.10.', 'Line 621 – again, please rephrase ‘This suggests..’ as it can be ambiguous.')
response('We rephrased the sentence so that its referent is explicit, and added a supporting reference.')
revised(f'Discussion, Section 4.4, {L("Taken together, these accounts suggest", "particular context [45].")}', Q('Taken together, these accounts suggest', 'particular context [45].'))

comment('Comment 2.11.', 'It is interesting that the age range of participants overall was 26 – 51 years. This may be a factor to add into the discussion and/or limitations. Does this reflect the general demographic of ICU nurses overall in the specific contexts?')
response('We added this to the Limitations. The lower bound reflects the eligibility requirement of at least one year of critical care experience. The absence of nurses older than 51 may reflect the exclusion of nurses in solely managerial roles and the voluntary recruitment. We did not have access to unit-level workforce data, so we cannot say whether the age profile matches that of ICU nurses at these hospitals, and the text states this plainly. We also note that age and career stage may shape engagement with the technology, so the experiences of late-career nurses and of novices may differ from those reported. The Conclusion now calls for research that includes nurses at both earlier and later career stages.')
revised(f'Discussion, Section 4.6, {L("Participants were aged 26 to 51", "differ from those reported here.")}', Q('Participants were aged 26 to 51', 'differ from those reported here.'))

comment('Closing remark.', 'Thank you.')
response('Thank you again for the constructive and thoughtful review.')

heading('FILES SUPPLIED WITH THIS RESUBMISSION')
for f in ['Response to the Editor and Reviewers (this document)',
          'Revised manuscript with changes highlighted',
          'Revised manuscript, clean copy',
          'Revised title page (highlighted and clean), including the AI-use statement in the Acknowledgements',
          'Supplementary File S1 (revised): participant demographic form and interview guide, with section labels corrected',
          'Supplementary File S2 (new): analytic trail from orienting framework to final themes',
          'Supplementary File S3 (new): completed COREQ checklist',
          'Figure 2 (redrawn) as a separate high-resolution file [AUTHOR: supply]']:
    bullet(f)

doc.save('Response_to_Editor_and_Reviewers.docx')
print('letter saved; quotes used:', len(USED))
