"""Build Supplementary Files S2 (analytic trail) and S3 (COREQ checklist) on the S1 template."""
import copy, re, zipfile, shutil
import docx
from lib import *

def base_doc(num, subtitle):
    d = docx.Document('s1_merged.docx')
    b = d.element.body
    kids = list(b)
    tmpl = {
        'title': kids[0], 'subtitle': kids[1], 'rule': kids[2],
        'study1': kids[3], 'study2': kids[4], 'table': kids[5],
        'h2': [k for k in kids if k.tag == W + 'p' and para_text(k).startswith('Section 1: Personal Details')][0],
        'body': [k for k in kids if k.tag == W + 'p' and para_text(k).startswith('Thank you for agreeing')][0],
    }
    tmpl = {k: copy.deepcopy(v) for k, v in tmpl.items()}
    sect = kids[-1]
    for k in kids[:-1]:
        b.remove(k)
    t = copy.deepcopy(tmpl['title']); t.find('.//' + W + 't').text = f'SUPPLEMENTARY FILE S{num}'
    s = copy.deepcopy(tmpl['subtitle']); s.find('.//' + W + 't').text = subtitle
    for el in (t, s, copy.deepcopy(tmpl['rule']), copy.deepcopy(tmpl['study1']), copy.deepcopy(tmpl['study2'])):
        sect.addprevious(el)
    return d, b, sect, tmpl

def add_para(sect, tmpl_p, segments):
    p = etree.Element(W + 'p')
    p.append(copy.deepcopy(tmpl_p.find(W + 'pPr')))
    rpr = first_plain_rpr(tmpl_p)
    for seg in segments:
        text, hl = seg[0], seg[1]; o = seg[2] if len(seg) > 2 else {}
        p.append(make_run(text, rpr, hl=hl, **o))
    sect.addprevious(p); return p

def add_heading(sect, tmpl, text):
    p = copy.deepcopy(tmpl['h2'])
    for r in p.findall(W + 'r')[1:]: p.remove(r)
    p.find('.//' + W + 't').text = text
    sect.addprevious(p); return p

PH = re.compile(r'(\[AUTHOR:[^\]]*\])')

def add_table(sect, tmpl, rows, widths, size=18):
    tbl = copy.deepcopy(tmpl['table'])
    for tr in tbl.findall(W + 'tr'): tbl.remove(tr)
    tbl.find(W + 'tblPr').find(W + 'tblW').set(W + 'w', str(sum(widths)))
    grid = tbl.find(W + 'tblGrid')
    for gc in grid.findall(W + 'gridCol'): grid.remove(gc)
    for w_ in widths:
        gc = etree.SubElement(grid, W + 'gridCol'); gc.set(W + 'w', str(w_))
    src_tr = tmpl['table'].findall(W + 'tr')[0]
    hdr_tc, body_tc = src_tr.findall(W + 'tc')
    for ri, row in enumerate(rows):
        tr = copy.deepcopy(src_tr)
        for tc in tr.findall(W + 'tc'): tr.remove(tc)
        for ci, txt in enumerate(row):
            tc = copy.deepcopy(hdr_tc if ri == 0 else body_tc)
            tcw = tc.find(W + 'tcPr').find(W + 'tcW'); tcw.set(W + 'w', str(widths[ci])); tcw.set(W + 'type', 'dxa')
            if ri > 0:
                shd = tc.find(W + 'tcPr').find(W + 'shd')
                if shd is not None: tc.find(W + 'tcPr').remove(shd)
            p = tc.find(W + 'p')
            for extra in tc.findall(W + 'p')[1:]: tc.remove(extra)
            jc = p.find(W + 'pPr').find(W + 'jc')
            if jc is not None: jc.set(W + 'val', 'left')
            rpr = p.find(W + 'r').find(W + 'rPr') if p.find(W + 'r') is not None else None
            for r in p.findall(W + 'r'): p.remove(r)
            lines = txt.split('\n')
            for li, line in enumerate(lines):
                pp = p if li == 0 else copy.deepcopy(p)
                if li:
                    for r in pp.findall(W + 'r'): pp.remove(r)
                    tc.append(pp)
                for part in PH.split(line):
                    if not part: continue
                    pp.append(make_run(part, rpr, hl=bool(PH.fullmatch(part)), bold=(ri == 0) or None, size=size))
            tr.append(tc)
        tbl.append(tr)
    sect.addprevious(tbl)
    return tbl

def finish(d, path, num):
    for t in d.element.body.iter(W + 't'):
        if t.text and t.text != t.text.strip(): t.set(XMLSP, 'preserve')
    d.save(path)
    # header: "Supplementary File S1 |" -> S{num}
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename.startswith('word/header'):
                data = data.replace(b'>1 |<', f'>{num} |<'.encode())
            zout.writestr(it, data)
    shutil.move(tmp, path)

# ------------------------------------------------------------------ S2
d, b, sect, T = base_doc(2, 'Analytic Trail: Orienting Framework, Areas of Inquiry, Initial Codes, and Final Themes')
add_heading(sect, T, 'Purpose of this file')
add_para(sect, T['body'], [('This file documents how the analysis moved from the areas of inquiry defined before data collection to the final interpretive themes. It distinguishes what was set in advance (the orienting conceptual framework shown in manuscript Figure 1 and the four areas of inquiry in the interview guide, Supplementary File S1) from what was developed through reflexive thematic analysis (initial codes, candidate themes, and final themes).', False)])
add_heading(sect, T, 'Analytic orientation')
add_para(sect, T['body'], [('The analysis combined deductive and inductive elements. The orienting framework acted as a sensitising device: it informed the four areas of inquiry and therefore what participants were asked about, but no codebook or predefined themes were applied. Initial codes were generated inductively from participants’ accounts at semantic and latent levels in NVivo 14. Codes were then clustered into candidate themes around central organising concepts, reviewed against the coded extracts and the full dataset, and refined through research team discussion, peer debriefing, and member checking (manuscript Sections 2.8 and 2.10). The four final themes broadly correspond to the four areas of inquiry because these areas structured the interviews; the interpretive content of each theme, summarised in the final column below, was developed through analysis.', False)])
add_heading(sect, T, 'Table S2.1. Analytic trail from orienting framework to final themes')
rows = [
 ['Final theme', 'Framework concepts (predefined, sensitising)', 'Area of inquiry and guide questions (predefined)', 'Illustrative initial codes (generated from the data)', 'Interpretation developed through analysis (not predefined)'],
 ['Theme 1. Learning to Read the Machine', 'AI-assisted early warning systems; alert fatigue; institutional support', 'Area 1: experiences of interacting with AI-assisted early warning (Q1–Q4)',
  'No one explained how it worked\nIs it replacing my assessment?\nEarly excitement turning to doubt\nLearning the system’s “personality”\nSenior colleagues translating alarms\nFiltering alerts automatically\nTriaging alerts before moving',
  'Engagement as an evolving, largely peer-mediated relationship rather than an outcome of implementation; peer calibration especially salient for internationally recruited nurses; scepticism as an early interpretive strategy among senior nurses (disconfirming cases); alert burden as learned prioritisation'],
 ['Theme 2. Between the Alert and the Bedside', 'Clinical judgment (noticing, interpreting, responding, reflecting); professional autonomy', 'Area 2: alert-informed clinical judgment and decision-making (Q5–Q9)',
  'Knowing the patient’s baseline\nAlert confirming a gut feeling\nDocumenting the reasoning for an override\nEscalating “to be safe”\nAlert as permission to call\nJudgment in seconds under workload\nLingering doubt after acting',
  'Three response modes (overriding, deferring, and negotiating), with negotiation as an expression of judgment rather than indecision; uncertainty carried beyond the moment of action; defensive alert management where non-action required documented justification (Hospital D)'],
 ['Theme 3. Alert, Action, and the Safety of the Patient', 'Patient safety practices; alert fatigue', 'Area 3: perceived implications for patient safety (Q10–Q12)',
  'Early flag on a lactate trend\nThe system does not get tired\nThe system “cries wolf”\nColleague stopped believing alerts\nThoughts of leaving the post\nCannot see the patient’s eyes\n“The safety net is us”',
  'Safety as co-produced by algorithmic surveillance and nursing judgment; perceived safety value contingent on nurses’ available attentional capacity; false alerts as a safety risk and a threat to work sustainability; the irreducible human layer of safety'],
 ['Theme 4. The Conditions That Shape the Space Between Alert and Action', 'Trust in AI; professional autonomy; institutional support and governance', 'Area 4: contextual and professional conditions (Q13–Q16)',
  'Trust is earned over time\nTrusting sepsis alerts more than respiratory alerts\nMy judgment has to argue with the alert\nAlert as one input among several\nTwo training sessions, then on your own\nAdapting is not being prepared\nSelf-directed learning',
  'Trust as situated, selective, and calibrated rather than a general attitude; governance shaping whether AI is experienced as supportive or supervisory; a gap between institutional preparation and the interpretive demands of the systems'],
]
add_table(sect, T, rows, [1500, 1600, 1600, 2300, 2360])
add_para(sect, T['body'], [('Note: Code labels are illustrative examples of codes developed during analysis and are presented as short descriptive labels. ', False, {'size': 18}),
                           ('[AUTHOR: verify each label against the NVivo codebook and, where they differ, replace with the exact code names.]', True, {'size': 18}),
                           (' Themes cut across the areas of inquiry: for example, alert burden was coded in accounts of first encounters, decision-making under pressure, and patient safety, and the Saudi practice context (Q16) informed Themes 1 and 4 rather than forming a separate theme. Q, question number in the interview guide (Supplementary File S1).', False, {'size': 18})])
finish(d, 'S2_Supplementary_Analytic_Trail.docx', 2)

# ------------------------------------------------------------------ S3
d, b, sect, T = base_doc(3, 'Consolidated Criteria for Reporting Qualitative Research (COREQ) Checklist')
add_para(sect, T['body'], [('Checklist items are from Tong, Sainsbury and Craig (2007). Locations refer to section numbers in the revised manuscript; page numbers are not given because they will change at typesetting.', False)])
C = [
 ['No.', 'Item', 'Location in manuscript', 'How the item is addressed'],
 ['', 'Domain 1: Research team and reflexivity', '', ''],
 ['1', 'Interviewer/facilitator', '2.5', 'All interviews were conducted by the principal investigator.'],
 ['2', 'Credentials', '2.5; title page', 'Nurse academic with postgraduate training in qualitative research [AUTHOR: state highest degree, e.g., PhD, RN].'],
 ['3', 'Occupation', '2.5', 'Nurse academic.'],
 ['4', 'Gender', '2.10', 'Male.'],
 ['5', 'Experience and training', '2.5; 2.10', 'Postgraduate training in qualitative research; clinical background in critical care and paediatric nursing.'],
 ['6', 'Relationship established', '2.10', 'No employment, managerial, supervisory, or teaching relationship with participating units or participants [AUTHOR: confirm].'],
 ['7', 'Participant knowledge of the interviewer', '2.5', 'Institutional affiliation and professional background disclosed at the start of each interview.'],
 ['8', 'Interviewer characteristics', '2.5; 2.10', 'Clinical familiarity, its potential influence, and reflexive strategies reported.'],
 ['', 'Domain 2: Study design', '', ''],
 ['9', 'Methodological orientation and theory', '2.1; 2.2', 'Interpretive Description with reflexive thematic analysis; orienting conceptual framework used as a sensitising heuristic.'],
 ['10', 'Sampling', '2.3', 'Purposive, criterion-based sampling seeking variation in experience, education, nationality, and site.'],
 ['11', 'Method of approach', '2.3; 2.9', 'Information sheet circulated by unit managers; interested nurses contacted the research team directly.'],
 ['12', 'Sample size', '2.3; 3.1', '23 registered nurses (5–6 per site).'],
 ['13', 'Non-participation', '2.3', '[AUTHOR: insert number and reasons, or state none].'],
 ['14', 'Setting of data collection', '2.5', 'Private rooms in participating hospitals or secure video.'],
 ['15', 'Presence of non-participants', '2.5', '[AUTHOR: confirm that no one other than the participant and interviewer was present].'],
 ['16', 'Description of sample', '3.1; Tables 1 and 2', 'Age, sex, nationality (aggregate), qualification, experience, site, and system exposure.'],
 ['17', 'Interview guide', '2.6; Supplementary File S1', 'Developed from framework and literature, expert-reviewed, and piloted with two nurses; full guide provided.'],
 ['18', 'Repeat interviews', '2.5', '[AUTHOR: confirm that no repeat interviews were conducted].'],
 ['19', 'Audio/visual recording', '2.7', 'All interviews audio-recorded with consent.'],
 ['20', 'Field notes', '2.5; 2.10', 'Post-interview reflexive field notes recorded in the reflexive journal.'],
 ['21', 'Duration', '2.6', '45–75 minutes (mean approximately 58 minutes).'],
 ['22', 'Data saturation', '2.3; 2.10', 'Interpretive sufficiency, rather than saturation, used as the adequacy criterion, consistent with Interpretive Description.'],
 ['23', 'Transcripts returned', '2.10', 'Transcripts were not returned; six participants reviewed summary accounts of the emerging themes [AUTHOR: confirm].'],
 ['', 'Domain 3: Analysis and findings', '', ''],
 ['24', 'Number of data coders', '2.8', 'Two: the principal investigator coded all transcripts; a second analyst independently coded three (13%).'],
 ['25', 'Description of the coding tree', '2.8; Table 3; Supplementary File S2', 'Themes and subthemes in Table 3; analytic trail from framework to themes in Supplementary File S2.'],
 ['26', 'Derivation of themes', '2.8; Supplementary File S2', 'Combined approach: predefined areas of inquiry; codes and themes developed inductively.'],
 ['27', 'Software', '2.8', 'NVivo 14 (Lumivero).'],
 ['28', 'Participant checking', '2.10', 'Member checking with six purposively selected participants.'],
 ['29', 'Quotations presented', 'Findings, Themes 1–4', 'Quotations identified by participant code, sex, banded experience, and site.'],
 ['30', 'Data and findings consistent', 'Findings; Discussion', 'Each subtheme is supported by quotations; disconfirming cases are reported.'],
 ['31', 'Clarity of major themes', 'Findings; Table 3; Figure 2', 'Four themes presented and illustrated.'],
 ['32', 'Clarity of minor themes', 'Findings', 'Subthemes and disconfirming patterns described within each theme.'],
]
tbl = add_table(sect, T, C, [700, 2500, 2300, 3860])
# shade domain rows like the header
for tr in tbl.findall(W + 'tr')[1:]:
    tcs = tr.findall(W + 'tc')
    if para_text(tcs[0]) == '' and para_text(tcs[1]).startswith('Domain'):
        for r in tcs[1].iter(W + 'r'):
            from lib import _rpr_set
            _rpr_set(r.find(W + 'rPr'), 'b'); _rpr_set(r.find(W + 'rPr'), 'bCs')
add_para(sect, T['body'], [('Reference: Tong A, Sainsbury P, Craig J. Consolidated criteria for reporting qualitative research (COREQ): a 32-item checklist for interviews and focus groups. Int J Qual Health Care. 2007;19:349–57. https://doi.org/10.1093/intqhc/mzm042.', False, {'size': 18})])
finish(d, 'S3_COREQ_Checklist.docx', 3)
print('built S2, S3')
