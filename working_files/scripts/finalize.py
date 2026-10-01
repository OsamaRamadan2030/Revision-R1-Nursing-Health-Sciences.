"""Fill author-input placeholders only (author-supplied data); no other text changes."""
import re, copy, docx
from lib import *
from lib import _rpr_set
d = docx.Document('Manuscript_Revised_Highlighted.docx'); body = d.element.body
def P(prefix):
    hits = [p for p in body.iter(W + 'p') if para_text(p).startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits)); return hits[0]
def sub_in_runs(p, old, new):
    """Replace text inside a single (highlighted) run; keeps its formatting."""
    for t in p.iter(W + 't'):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new); return
    raise AssertionError('not found: ' + old[:60])

# 2.3 definition: drop the unknown-source placeholder clause
p = P('For this study, AI-assisted early warning systems were defined')
sub_in_runs(p, ' Site-level information was obtained from [AUTHOR: insert source, e.g., hospital nursing informatics departments]; vendor and product names are withheld to preserve institutional anonymity.', ' Vendor and product names are withheld to preserve institutional anonymity.')

# Table 1 values (author-supplied)
T1 = {
 2: ['Multivariable machine-learning models estimate sepsis and respiratory deterioration risk from vital signs, laboratory results and clinical records.', 'Multivariable machine-learning model estimates general deterioration risk from vital-sign trends, laboratory results and clinical records.', 'Multivariable machine-learning models estimate sepsis and respiratory deterioration risk from longitudinal physiological and laboratory data.', 'Multivariable machine-learning model estimates general deterioration risk, incorporating vital signs and laboratory trends, including lactate.'],
 3: ['Sepsis risk; respiratory deterioration risk', 'Composite deterioration risk; persistent high-risk trend', 'Sepsis risk; respiratory deterioration risk', 'Composite deterioration risk; worsening multivariable trend'],
 4: ['Electronic record risk panel and central dashboard; bedside nurse reviews and discusses with charge nurse.', 'Central dashboard and electronic record notification; bedside nurse acknowledges and informs charge nurse.', 'Electronic record risk panel and bedside workstation notification; nurse reviews trends and escalates concerns.', 'Central dashboard and electronic record task list; bedside and charge nurses review; response is documented.'],
 5: ['January 2023; 36 months', 'January 2024; 24 months', 'July 2023; 30 months', 'July 2022; 42 months'],
 6: ['One demonstration and quick-reference guide; peer support thereafter.', 'Two introductory sessions; attendance varied; limited refresher support.', 'One workshop and case examples; peer coaching thereafter.', 'One orientation on alerts and documentation; support through unit educators.'],
 7: ['Bedside assessment and trend review; escalate according to clinical concern; record response and rationale.', 'Acknowledge and assess; inform charge nurse and escalate concerns; document the assessment.', 'Assess the patient and trends; discuss discordant alerts with the treating team; document the response.', None],
 8: ['1 / 1 / 3 / 0', '1 / 2 / 3 / 0', '1 / 1 / 4 / 0', '0 / 1 / 3 / 2'],
 9: ['3 (60.0)', '4 (66.7)', '3 (50.0)', '4 (66.7)'],
 10: ['2 (40.0)', '2 (33.3)', '3 (50.0)', '2 (33.3)'],
}
LABELS = {5: 'Time since implementation at data collection (January 2026)', 8: 'Participants’ duration of system use, n (<6 months / 6–12 months / >12–36 months / >36 months)', 9: 'Participants reporting formal training on the system, n (% within site)', 10: 'Participants with prior experience of similar systems elsewhere, n (% within site)'}
cap = P('Table 1. Characteristics of AI-Assisted'); tbl = cap.getnext(); rows = tbl.findall(W + 'tr')
def setcell(tc, v):
    pp = tc.findall(W + 'p')
    for extra in pp[1:]: tc.remove(extra)
    rpr = pp[0].find(W + 'r').find(W + 'rPr')
    for rr in pp[0].findall(W + 'r'): pp[0].remove(rr)
    pp[0].append(make_run(v, rpr, hl=True))
for ri, vals in T1.items():
    tcs = rows[ri].findall(W + 'tc')
    for tc, v in zip(tcs[1:], vals):
        if v is not None: setcell(tc, v)
    if ri in LABELS: setcell(tcs[0], LABELS[ri])
note = tbl.getnext()
sub_in_runs(note, 'Note: Participant exposure data are from the demographic form (Supplementary File S1). Vendor and product names are withheld to protect institutional anonymity. The Hospital D protocol is as described by participants [AUTHOR: confirm against the written protocol]. AI, artificial intelligence.',
 'Note: Participant exposure data are from the demographic form (Supplementary File S1); percentages use the site denominator. Overall, system use was <6 months for 3 (13.0%), 6–12 months for 5 (21.7%), >12–36 months for 13 (56.5%) and >36 months for 2 (8.7%) participants; 14/23 (60.9%) reported formal training and 9/23 (39.1%) prior experience of similar systems. Formal training denotes attendance at a scheduled session, not verified competence. The Hospital D protocol is as described by participants and was not checked against a written policy. Vendor and product names are withheld to protect institutional anonymity. AI, artificial intelligence.')

# 2.3 recruitment
p = P('Recruitment was facilitated through nursing administration')
sub_in_runs(p, ' Data were collected between [AUTHOR: Month YYYY] and [AUTHOR: Month YYYY]. [AUTHOR: state how many nurses contacted the research team and the number of, and reasons for, any who were ineligible, declined, or withdrew; if none, state that all nurses who volunteered and met the eligibility criteria were interviewed and none withdrew.]',
 ' Data were collected from January to March 2026. Of the 26 nurses who contacted the research team, three were ineligible because they had less than one year of critical care experience; no eligible volunteer declined, and no participant withdrew.')
# 2.5
p = P('Data were generated through individual, semi-structured')
sub_in_runs(p, 'Overall, [AUTHOR: n] interviews were conducted face-to-face and [AUTHOR: n] by video; [AUTHOR: n] were conducted in Arabic and [AUTHOR: n] in English.', 'Overall, 15 interviews were conducted face-to-face and eight by video; 14 were conducted in Arabic and nine in English.')
sub_in_runs(p, ' [AUTHOR: confirm both statements]', '')
# 2.10
sub_in_runs(P('Methodological rigour was established'), ' [AUTHOR: confirm]', '')
p = P('The principal investigator is a male nurse academic')
sub_in_runs(p, 'with a clinical background in critical care and paediatric nursing [AUTHOR: specify roles and years, e.g., “six years as an adult ICU staff nurse”].', 'with six years of adult intensive care nursing experience and three years of paediatric nursing experience.')
sub_in_runs(p, ' [AUTHOR: confirm; if any prior relationship existed, state how it was managed]', '')

# Figure 2: new image, remove placeholder line, legend
ph = P('[AUTHOR: replace the image above'); img_p = ph.getprevious(); ph.getparent().remove(ph)
blip = list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))[0]
rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
d.part.related_parts[rid]._blob = open('Figure2_revised.png', 'rb').read()
for ext in list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')) + list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}ext')):
    if ext.get('cx'): ext.set('cy', str(int(int(ext.get('cx')) * 6.1 / 6.69)))
p = P('Figure 2. Thematic map')
sub_in_runs(p, 'The figure was created by the authors; no artificial intelligence tools were used in its creation or enhancement.' if 'The figure was created' in para_text(p) else 'No artificial intelligence tools were used to create or enhance this figure.',
 'The figure was redrawn during revision using AI-assisted plotting code generated from the authors’ thematic structure (Table 3) and was checked by the authors.')

# reference 47: completed bibliographic details (previously incomplete)
p = P('47. Yanto A')
sub_in_runs(p, 'A Philosophical and Professional Perspective. 2025.', 'A Philosophical and Professional Perspective. Research Square [Preprint]. 2025. https://doi.org/10.21203/rs.3.rs-7975002/v1.')

left = [para_text(x)[:90] for x in body.iter(W + 'p') if '[AUTHOR' in para_text(x)]
print('leftover placeholders:', left)
for t in body.iter(W + 't'):
    if t.text and t.text != t.text.strip(): t.set(XMLSP, 'preserve')
d.save('Manuscript_Revised_Highlighted.docx'); print('saved')
