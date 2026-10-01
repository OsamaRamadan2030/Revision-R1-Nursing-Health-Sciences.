import copy, re, sys
import docx
from lxml import etree
from lib import *

SRC = 'work_merged.docx'
OUT = 'Manuscript_Revised_Highlighted.docx'
d = docx.Document(SRC)
body = d.element.body
print('fields unlinked:', unlink_fields(body))

def H(t, **o): return (t, True, o)
def U(t, **o): return (t, False, o)

def P(prefix):
    hits = [p for p in body.iter(W + 'p') if para_text(p).startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

def label_seg(p_el):
    """Return (label_text, label_rPr) for a paragraph starting with a bold label run."""
    r = p_el.find(W + 'r')
    return r.find(W + 't').text, r.find(W + 'rPr')

TEMPLATE_BODY = P('This study used a qualitative design informed by')  # body paragraph pPr

# ---------------------------------------------------------------- Abstract
p = P('Design: A qualitative study informed by')
set_segments(p, [H(' A qualitative study informed by Interpretive Description and reported in accordance with the Consolidated Criteria for Reporting Qualitative Research (COREQ).')], keep_first_n=1)

p = P('Methods: Semi-structured interviews were conducted with 23')
set_segments(p, [H(' Semi-structured interviews were conducted with 23 purposively sampled registered nurses across four tertiary hospitals in northern Saudi Arabia that used AI-assisted early warning systems. Data were analysed using reflexive thematic analysis, combining inductive coding with sensitising concepts from an orienting conceptual framework.')], keep_first_n=1)

p = P('Conclusion: AI-assisted early warning did not replace')
set_segments(p, [U(' AI-assisted early warning did not replace nursing judgment. Its value depended on nurses’ capacity to interpret alerts within bedside realities.'),
                 H(' The findings suggest that safe implementation depends on structured training, supportive governance, and attention to alert fatigue.')], keep_first_n=1)

p = P('Safe use of AI-assisted early warning in critical care requires')
set_segments(p, [H('Safe use of AI-assisted early warning in critical care is likely to depend on structured education, supportive governance, and explicit attention to alert fatigue and nurses’ decision-making authority.')])

# ---------------------------------------------------------------- Introduction
p = P('The integration of artificial intelligence (AI) into critical care')
set_segments(p, [
    U('The integration of artificial intelligence (AI) into critical care settings is reshaping how deterioration is detected, interpreted, and acted upon in contemporary nursing practice [1, 2]. Among the most prominent developments are AI-assisted early warning systems, which analyse physiological and clinical data to identify early signs of patient deterioration and generate alerts to support timely clinical response [3].'),
    H(' Unlike conventional single-parameter monitor alarms and rule-based aggregate scores, which trigger alerts when fixed thresholds are crossed, AI-assisted systems apply machine-learning or other data-driven predictive models to multiple, continuously updated data sources to generate patient-specific risk estimates [[R8,R11]].'),
    U(' These systems are increasingly embedded within intensive care unit (ICU) workflows as part of broader efforts to enhance surveillance, support timely intervention, and improve patient safety [4, 5].'),
    H(' However, their rapid implementation has outpaced understanding of how nurses, who remain central to bedside monitoring, escalation, and rescue, experience and use these tools in everyday practice [[R6]].'),
    U(' Although AI-assisted early warning systems are intended to strengthen clinical decision-making, their effectiveness in practice depends not only on algorithmic performance but also on how nurses interpret, trust, question, and act on algorithm-generated alerts [7, 8].')])

p = P('Existing research on early warning technologies')
set_segments(p, [
    H('Existing research on early warning technologies has focused predominantly on predictive accuracy, system performance, implementation feasibility, and general clinician attitudes toward AI-enabled tools [[R9,R10,R45]].'),
    U(' This body of work has demonstrated the potential of machine-learning-based surveillance systems, sepsis prediction tools, and continuously monitored alert platforms to improve the timeliness of detecting deterioration in acute care environments [11]. At the same time, concerns remain regarding false positives, limited specificity, workflow disruption, and alert fatigue, all of which may undermine responsiveness to clinically important warnings [12, 13]. For critical care nurses, AI-generated alerts do not function in isolation; rather, they enter an already complex clinical environment in which nurses must integrate algorithmic output with bedside assessment, contextual knowledge of the patient, and professional judgment [14, 15].'),
    H(' Yet this interpretive work has rarely been examined from the perspective of nurses themselves, particularly as a real-time practice phenomenon situated at the intersection of alert interpretation, clinical reasoning, and patient safety.')])

p = P('The Saudi Arabian healthcare context gives')
set_segments(p, [
    U('The Saudi Arabian healthcare context gives this inquiry particular relevance.'),
    H(' Vision 2030, launched in 2016, is Saudi Arabia’s national strategic framework for economic diversification and the modernisation of public services; its Health Sector Transformation Program aims to restructure the health system to improve access, quality, and efficiency, including through the expansion of e-health and digital services [[N1]]. Within this agenda, digital health transformation and AI integration have become strategic national priorities, with substantial investment in smart hospital infrastructure, advanced monitoring technologies, and intelligent clinical decision-support systems [[R30,R31]].'),
    U(' Within critical care settings, these developments unfold in a socio-professional environment characterised by rapid technological expansion, a multinational nursing workforce, evolving nursing leadership, and the ongoing development of professional roles and decision-making authority [32]. These contextual features may shape how AI-generated alerts are understood, trusted, and translated into action in practice [33]. Despite growing technological adoption in the Kingdom, there remains limited qualitative evidence on how critical care nurses in Saudi Arabia experience AI-assisted early warning systems and how these systems influence clinical judgment and patient safety practices [34–36]. Addressing this gap is important for informing nursing education, implementation strategies, technology governance, and the safe integration of AI into critical care services.')])

# ---------------------------------------------------------------- Methods
p = P('This study used a qualitative design informed by')
set_segments(p, [
    H('This study used a qualitative design informed by Interpretive Description (ID) [[R37,R38]] to explore how critical care nurses in Saudi Arabia experience AI-assisted early warning systems in relation to clinical judgment and patient safety.'),
    U(' ID was selected because the study sought to generate clinically meaningful, practice-relevant interpretive insights rather than a phenomenological description or a formal theory. This made it more appropriate than phenomenological approaches, grounded theory, or generic qualitative description for the present nursing-focused inquiry.'),
    H(' Data were analysed using reflexive thematic analysis as described by Braun and Clarke [[N5,R39]], which provided a flexible and rigorous analytic approach consistent with the interpretive logic of ID. Reporting followed the Consolidated Criteria for Reporting Qualitative Research (COREQ) [[R40,R41]]; the completed checklist is provided in Supplementary File S3.')])

p = P('The study was guided by an orienting conceptual framework')
set_segments(p, [
    U('The study was guided by an orienting conceptual framework (Figure 1) that positioned nurses’ experiences at the intersection of AI-assisted early warning systems, clinical judgment, and patient safety practices.'),
    H(' The framework was developed by the authors from three bodies of work: Tanner’s model of clinical judgment, which describes judgment as noticing, interpreting, responding, and reflecting, shaped by what the nurse brings to the situation and by knowing the patient [[N2]]; sociotechnical perspectives, which view safety as emerging from interactions among technology, people, workflow, and organisational policy [[N3]]; and research on trust in automation and AI-based decision support and on alarm fatigue [[N4,R10,R65]]. Drawing on this literature, the framework identified trust in AI, alert fatigue, professional autonomy, and institutional support and governance as potentially relevant contextual influences.'),
    U(' Consistent with Interpretive Description, the framework was used as a sensitising heuristic to inform interview development and analytic attention, rather than as a prescriptive or causal model [43, 44].'),
    H(' It defined the broad areas of inquiry explored in the interviews but did not specify codes or themes in advance (Section 2.8).')])

p = P('Figure 1. Orienting conceptual framework')
lab_rpr = p.findall(W + 'r')[1].find(W + 'rPr')
p.append(make_run('. The framework was developed by the authors as a non-causal sensitising heuristic, drawing on Tanner’s clinical judgment model [[N2]], sociotechnical perspectives on health information technology [[N3]], and literature on trust in automation and alarm fatigue [[N4,R65]]. The figure was created by the authors; no artificial intelligence tools were used in its creation or enhancement.', lab_rpr, hl=True))

# 2.3 setting: definition paragraph + new Table 1
p_set = P('The study was conducted across four tertiary-level hospitals')
p_def = new_para_after(p_set, p_set, [H('For this study, AI-assisted early warning systems were defined as systems that apply machine-learning or other data-driven predictive algorithms to multiple, continuously updated physiological, laboratory, and clinical data to generate patient-specific deterioration risk estimates or alerts. Conventional single-parameter monitor alarms and rule-based aggregate early warning scores that apply fixed thresholds were not considered AI-assisted, although conventional monitor alarms operated alongside the AI-assisted systems in all participating units. The AI-assisted systems in use at each site, including their purpose, AI component, alert types, integration into nursing workflow, duration of implementation, training provision, and local response protocols, are summarised in Table 1, together with participants’ self-reported duration of system use, training, and prior experience with similar systems. Site-level information was obtained from [AUTHOR: insert source, e.g., hospital nursing informatics departments and vendor technical documentation]. Vendor and product names are withheld to preserve institutional anonymity.')])

old_cap = P('Table 1. Demographic and Professional Characteristics')
cap_label_rpr = old_cap.findall(W + 'r')[0].find(W + 'rPr')
cap_text_rpr = old_cap.findall(W + 'r')[1].find(W + 'rPr')
cap = etree.Element(W + 'p'); cap.append(copy.deepcopy(old_cap.find(W + 'pPr')))
cap.append(make_run('Table 1.', cap_label_rpr, hl=True))
cap.append(make_run(' Characteristics of AI-Assisted Early Warning Systems and Participants’ Exposure, by Hospital Site (N = 23)', cap_text_rpr, hl=True))
p_def.addnext(cap)

# Build new Table 1 from the participants' table XML conventions
old_t1 = d.tables[0]._tbl
hdr_tc = old_t1.findall(W + 'tr')[0].findall(W + 'tc')[0]
body_tc = old_t1.findall(W + 'tr')[1].findall(W + 'tc')[0]

def cell(text, header=False, left=False, width=None, hl=True):
    tc = copy.deepcopy(hdr_tc if header else body_tc)
    tcw = tc.find(W + 'tcPr').find(W + 'tcW')
    if width:
        tcw.set(W + 'w', str(width)); tcw.set(W + 'type', 'dxa')
    pp = tc.find(W + 'p')
    ppr = pp.find(W + 'pPr')
    if ppr.find(W + 'bidi') is None:
        bd = etree.Element(W + 'bidi'); bd.set(W + 'val', '0')
        sp = ppr.find(W + 'spacing')
        (sp.addprevious(bd) if sp is not None else ppr.insert(0, bd))
    rpr = pp.find(W + 'r').find(W + 'rPr')
    if left:
        jc = pp.find(W + 'pPr').find(W + 'jc'); jc.set(W + 'val', 'left')
    for r in pp.findall(W + 'r'):
        pp.remove(r)
    for i, line in enumerate(text.split('\n')):
        if i:
            pp = copy.deepcopy(pp); [pp.remove(r) for r in pp.findall(W + 'r')]; tc.append(pp)
        pp.append(make_run(line, rpr, hl=hl))
    return tc

A = '[AUTHOR: insert]'
t1_rows = [
    ['Characteristic', 'Hospital A', 'Hospital B', 'Hospital C', 'Hospital D'],
    ['Participants, n', '5', '6', '6', '6'],
    ['AI-assisted system: purpose and AI component', A, A, A, A],
    ['Principal alert types', A, A, A, A],
    ['Integration into nursing workflow (alert display and routing)', A, A, A, A],
    ['Time since implementation at data collection', A, A, A, A],
    ['Training provided at implementation', A, A, A, A],
    ['Local response protocol', A, A, A, 'Documented justification required when an alert is not acted upon'],
    ['Participants’ duration of system use, n (<6 months / 6–12 months / 1–3 years / >3 years)', A, A, A, A],
    ['Participants reporting formal training on the system, n', A, A, A, A],
    ['Participants with prior experience of similar systems elsewhere, n', A, A, A, A],
]
widths = [2540, 1750, 1750, 1750, 1750]
tbl = copy.deepcopy(old_t1)
for tr in tbl.findall(W + 'tr'):
    tbl.remove(tr)
grid = tbl.find(W + 'tblGrid')
for gc in grid.findall(W + 'gridCol'):
    grid.remove(gc)
for w_ in widths:
    gc = etree.SubElement(grid, W + 'gridCol'); gc.set(W + 'w', str(w_))
tmpl_tr = old_t1.findall(W + 'tr')[1]
for ri, row in enumerate(t1_rows):
    tr = copy.deepcopy(tmpl_tr)
    for tc in tr.findall(W + 'tc'):
        tr.remove(tc)
    for ci, txt in enumerate(row):
        tr.append(cell(txt, header=(ri == 0), left=(ci == 0 or ri > 1), width=widths[ci]))
    tbl.append(tr)
cap.addnext(tbl)

note_rpr = copy.deepcopy(first_plain_rpr(p_set))
note = new_para_after(tbl, old_cap, [H('Note: Site-level information was obtained from [AUTHOR: insert source]; participant data were drawn from the demographic form (Supplementary File S1). Vendor and product names are withheld to protect institutional anonymity. The response protocol at Hospital D is as described by participants [AUTHOR: confirm against the written hospital protocol]. AI, artificial intelligence.', size=20)], base_rpr=note_rpr)

p = P('Recruitment was facilitated through nursing administration')
set_segments(p, [
    U('Recruitment was facilitated through nursing administration offices following ethical approval. Unit managers circulated the participant information sheet to eligible staff, and nurses who wished to participate contacted the research team directly. Eligibility was then confirmed, and interviews were scheduled. No incentives were offered. A total of 23 critical care nurses participated.'),
    H(' Data were collected between [AUTHOR: Month YYYY] and [AUTHOR: Month YYYY]. [AUTHOR: state how many nurses contacted the research team and the number of, and reasons for, any who were ineligible, declined, or withdrew; if none, state that all nurses who volunteered and met the eligibility criteria were interviewed and none withdrew.]'),
    U(' In keeping with Interpretive Description, sample adequacy was judged by interpretive sufficiency rather than data saturation.'),
    H(' Interpretive sufficiency was considered achieved when the dataset provided a sufficiently rich and contextually detailed basis for robust interpretive analysis across participants, sites, and experience levels [[R37,R44]].')])

p = P('Data were generated through individual, semi-structured')
set_segments(p, [
    U('Data were generated through individual, semi-structured, in-depth interviews, which were appropriate for exploring nurses’ experiences with AI-generated alerts, their interpretation of these alerts, and the influence of these alerts on clinical judgment and patient safety practices. Interviews were conducted face-to-face in private rooms within the participating hospitals. When in-person interviews were not feasible due to shift-scheduling constraints, secure video interviews were conducted with participants\' consent.'),
    H(' Overall, [AUTHOR: n] interviews were conducted face-to-face and [AUTHOR: n] by video; [AUTHOR: n] were conducted in Arabic and [AUTHOR: n] in English. Before each interview, participants completed a brief demographic form capturing age, sex, nationality, years of critical care experience, highest educational qualification, the AI-assisted system used in their unit, duration of use of that system, training received, and prior experience with similar systems elsewhere (Supplementary File S1).'),
    U(' Written informed consent was obtained immediately before interview commencement. All interviews were conducted by the principal investigator, a nurse academic with postgraduate training in qualitative research and professional expertise in critical care and paediatric nursing. His institutional affiliation and professional background were disclosed to participants at the outset of each interview as part of reflexive transparency. Participants were encouraged to share views that differed from the researcher’s assumptions, and post-interview reflexive field notes were recorded as part of the reflexive journal to examine possible influences on data generation.')])

p = P('The final guide covered participants')
orig = para_text(p)
m = re.search(r'Example questions included:.*?approximately 58 minutes\.', orig)
set_segments(p, [
    U('The final guide covered participants’ experiences working with AI-assisted early warning systems; how they interpreted and responded to alerts; instances of concordance or discordance between AI alerts and bedside assessments; the influence of alerts on decision-making under uncertainty; perceived implications for patient safety; and contextual factors shaping trust and responsiveness.'),
    H(' These topics were organised into four areas of inquiry derived from the study objectives and the orienting framework, followed by closing questions. During data collection, the guide sections were labelled by area of inquiry only; they were not linked to themes, which were developed during analysis (Section 2.8).'),
    U(' ' + m.group(0)),
    H(' The full interview guide and demographic form are provided in Supplementary File S1.')])

p = P('Data were analysed using reflexive thematic analysis within')
set_segments(p, [
    H('Data were analysed using reflexive thematic analysis within the interpretive logic of Interpretive Description [[N5,R39]].'),
    U(' Analysis followed six phases: familiarisation with the data, generation of initial codes, development of candidate themes, review of themes against the full dataset, refinement and naming of themes, and production of the final analytic narrative.')])

p = P('The principal investigator conducted primary coding')
a1 = new_para_after(p, p, [H('The analysis combined deductive and inductive elements. Deductively, the orienting framework informed the four areas of inquiry in the interview guide and therefore what participants were invited to discuss; no codebook or predefined themes were applied. Inductively, initial codes were generated from participants’ accounts at both semantic and latent levels, and candidate themes were developed around central organising concepts that captured shared patterns of meaning across the dataset, rather than as summaries of responses to particular questions. The final themes broadly correspond to the four areas of inquiry, which is to be expected given that these areas structured the interviews; the interpretive content of each theme, however, was generated through analysis. Interpretations that were not anticipated by the framework or the interview questions include peer-mediated calibration as the main route through which nurses learned to use the systems, scepticism as an early interpretive strategy among senior nurses, negotiation as a third response mode alongside overriding and deferring, the dependence of the perceived safety value of AI on nurses’ available attentional capacity, and the defensive documentation associated with protocols that required justification of non-action. Supplementary File S2 traces, for each theme, the relationships among the framework concepts, the areas of inquiry, illustrative initial codes, and the final interpretation.')])
a2 = new_para_after(a1, p, [H('Site-level differences in system type, exposure, training, and response protocols (Table 1) were treated as interpretive context rather than as variables for comparison. Coded extracts were tagged by site, and analytic memos examined how accounts of alert interpretation, trust, and escalation related to local protocols, training, and length of exposure. This informed, for example, the interpretation of the more defensive orientation to alert management described at Hospital D, where non-action required documented justification, and of the more collaborative stance described by participants at Hospital A.')])

p = P('Ethical approval was obtained from the Institutional Review Board')
orig = para_text(p)
first = 'Ethical approval was obtained from the Institutional Review Board of XXX University and from the ethics committees of the four participating hospitals before recruitment or data collection began.'
assert orig.startswith(first)
set_segments(p, [
    H('Ethical approval was obtained from the Institutional Review Board of XXX University (reference number withheld for blinded review) and from the ethics committees of the four participating hospitals before recruitment or data collection began.'),
    U(orig[len(first):])])

p = P('Confirmability was strengthened through reflexive journaling')
new_para_after(p, p, [H('The principal investigator is a male nurse academic whose clinical background is in critical care and paediatric nursing [AUTHOR: specify previous clinical roles and approximate years of practice, e.g., “who worked as an adult ICU staff nurse for X years before entering academia”]. He had no employment, managerial, supervisory, or teaching relationship with the participating units or participants and had not worked at any of the four hospitals [AUTHOR: confirm; if any participant was a former student or colleague, state this and how it was managed]. His clinical familiarity with critical care supported rapport and the understanding of clinical terminology but also risked the assumption of shared meanings. He therefore invited participants to explain situations and terms in their own words and recorded in the reflexive journal instances in which his clinical assumptions shaped follow-up questions; these entries were reviewed in research team meetings.')])

# ---------------------------------------------------------------- Findings
p = P('The study participants ranged in age from 26 to 51 years')
orig = para_text(p)
tail = ' Participant characteristics are presented in Table 1. '
assert orig.endswith(tail), repr(orig[-80:])
set_segments(p, [U(orig[:-len(tail)]),
                 H(' Participant characteristics are presented in Table 2, and participants’ exposure to the AI-assisted systems is summarised by site in Table 1.')])

p = P('Table 1. Demographic and Professional Characteristics')
r0 = p.findall(W + 'r')[0]
p.replace(r0, make_run('Table 2. ', r0.find(W + 'rPr'), hl=True))

p = P('The sample was predominantly female')
set_segments(p, [
    H('Slightly more than half of the participants were female (n = 12, 52%), and the sample included participants from six nationalities:'),
    U(' Saudi Arabia (n = 7), the Philippines (n = 5), Jordan (n = 3), Egypt (n = 3), India (n = 3), and Sudan (n = 2). Critical care experience ranged from 2 to 23 years. Most participants held a Bachelor of Science in Nursing (BSN; n = 17), five held a Master of Science in Nursing (MSN), and one held a doctoral qualification.'),
    H(' All four hospital sites were represented, with five or six participants per site.')])

# Participants' table (old Table 1, now Table 2): drop nationality, band experience, merge postgraduate
def band(y):
    y = int(y)
    return '≤5' if y <= 5 else '6–10' if y <= 10 else '11–15' if y <= 15 else '>15'

pt = old_t1
grid = pt.find(W + 'tblGrid'); gcs = grid.findall(W + 'gridCol')
grid.remove(gcs[3])
for ri, tr in enumerate(pt.findall(W + 'tr')):
    tcs = tr.findall(W + 'tc')
    tr.remove(tcs[3])
    if ri == 0:
        continue
    q, e = tcs[4], tcs[5]
    for tc, newtxt in ((q, None), (e, band(para_text(tcs[5].find(W + 'p'))))):
        pp = tc.find(W + 'p'); txt = para_text(pp)
        if tc is q:
            newtxt = 'Postgraduate' if txt in ('MSN', 'PhD') else None
        if newtxt is None:
            continue
        rpr = pp.find(W + 'r').find(W + 'rPr')
        for r in pp.findall(W + 'r'): pp.remove(r)
        pp.append(make_run(newtxt, rpr, hl=True))
# widen remaining columns proportionally (keep total width)
ws = [705, 864, 1110, 2058, 2199, 1326]; extra = 1268
ws = [w_ + round(extra * w_ / sum(ws)) for w_ in ws]
for gc, w_ in zip(grid.findall(W + 'gridCol'), ws):
    gc.set(W + 'w', str(w_))
hdr = pt.findall(W + 'tr')[0].findall(W + 'tc')[4].find(W + 'p')
rpr = hdr.find(W + 'r').find(W + 'rPr')
for r in hdr.findall(W + 'r'): hdr.remove(r)
hdr.append(make_run('ICU experience (years, banded)', rpr, hl=True))
new_para_after(pt, old_cap, [H('Note: To protect participant confidentiality, nationality is reported only in aggregate in the text, critical care experience is presented in bands, and postgraduate qualifications are combined. BSN, Bachelor of Science in Nursing; ICU, intensive care unit; Postgraduate, Master of Science in Nursing (n = 5) or doctoral degree (n = 1).', size=20)], base_rpr=note_rpr)

p = P('Analysis of the 23 interview transcripts generated')
orig = para_text(p); tail = ' The thematic structure is presented in Table 2. '
assert orig.endswith(tail), repr(orig[-60:])
set_segments(p, [U(orig[:-len(tail)]), H(' The thematic structure is presented in Table 3.')])

p = P('Table 2. Interpretive Themes and Subthemes')
r0 = p.findall(W + 'r')[0]
p.replace(r0, make_run('Table 3. ', r0.find(W + 'rPr'), hl=True))

p = P('Nurses with fewer than five years of critical care experience (n = 7)')
set_segments(p, [H('Nurses with five or fewer years of critical care experience (n = 6) described placing greater initial weight on alert outputs in situations of uncertainty, whereas more experienced nurses described a more sceptical and bidirectional interpretive stance.')])

p = P('Nurses working in better-staffed contexts')
set_segments(p, [
    U('Nurses working in better-staffed contexts described AI more often as confirming rather than revealing deterioration.'),
    H(' These accounts suggest that the perceived safety value of AI-assisted early warning was shaped by available attentional capacity, with the technology experienced as most beneficial when nurses’ surveillance resources were constrained.'),
    U(' A disconfirming pattern was evident among a smaller group of nurses who felt their own surveillance capacity was sufficient and viewed alerts primarily as reinforcement rather than added protection.')])

# quote attributions: band years of experience
pat = re.compile(r'\((P\d\d), (female|male), (\d+) years’ experience, (Hospital [A-D])\)')
n_attr = 0
for pp in body.iter(W + 'p'):
    for r in list(pp.findall(W + 'r')):
        for t in r.findall(W + 't'):
            if not t.text: continue
            m = pat.search(t.text)
            if not m: continue
            assert t is r.findall(W + 't')[-1]
            before, after = t.text[:m.start()], t.text[m.end():]
            rpr = r.find(W + 'rPr')
            t.text = before
            newr = [make_run(f'({m.group(1)}, {m.group(2)}, {band(m.group(3))} years’ experience, {m.group(4)})', rpr, hl=True, italic=False)]
            if after: newr.append(make_run(after, rpr))
            for nr in reversed(newr): r.addnext(nr)
            if not ''.join(x.text or '' for x in r.findall(W + 't')):
                pp.remove(r)
            n_attr += 1
print('attributions banded:', n_attr)

# Figure 2
p = P('Figure 2. Thematic map')
lab_rpr = p.findall(W + 'r')[1].find(W + 'rPr')
p.append(make_run('. Themes are shown with their subthemes; connecting lines indicate interpretive relationships between themes rather than causal pathways. The figure was created by the authors; no artificial intelligence tools were used in its creation or enhancement.', lab_rpr, hl=True))
img_p = p.getprevious()
while img_p is not None and not list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip')):
    img_p = img_p.getprevious()
assert img_p is not None
ph = etree.Element(W + 'p'); ph.append(copy.deepcopy(p.find(W + 'pPr')))
ph.append(make_run('[AUTHOR: replace the image above with the redrawn Figure 2 before submission; see “Figure 2 redraw specification” in the Final Audit Report.]', lab_rpr, hl=True, italic=False))
img_p.addnext(ph)

# ---------------------------------------------------------------- Discussion
p = P('The findings showed that engagement with AI-assisted early warning')
set_segments(p, [
    U('The findings showed that engagement with AI-assisted early warning was not established at implementation but developed through repeated exposure, peer interaction, and practical calibration. Initial uncertainty, particularly among less experienced nurses, suggests that early use of AI may heighten rather than reduce anxiety when the meaning of alerts is unclear.'),
    H(' Earlier work has largely conceptualised technology acceptance as an attitude or intention assessed at, or soon after, the point of adoption [[N6,R7,R34,R59]]; the present findings extend this work by showing that acceptance is not a fixed starting point but an experience shaped through everyday practice, consistent with frameworks that emphasise the continuing mutual adaptation of technologies, users, and organisations over time [[N7]]. In the Saudi context, where internationally recruited nurses form a large proportion of the nursing workforce [[N11]], this process may be further complicated for nurses who must adapt simultaneously to a new organisational and cultural environment [[N8]] and to a new digital system. The prominence of peer-mediated learning is consistent with accounts of clinical expertise as developed through experience and shared practical knowledge [[N9]], and suggests that informal socialisation remains central to how AI becomes usable in practice, while also introducing variability in the quality of knowledge transfer. These findings point to the need for structured onboarding.'),
    U(' Alert burden was another defining feature of this evolving relationship.'),
    H(' Participants’ accounts align with the alarm-fatigue literature [[R61,R65]] and indicate that alert fatigue was experienced not only as attentional depletion but also as a professional and emotional burden linked to system design and workload conditions [[R62]].')])

p = P('AI-assisted early warning did not simplify clinical judgment')
set_segments(p, [
    U('AI-assisted early warning did not simplify clinical judgment; instead, it introduced an additional layer of interpretation. Nurses described balancing algorithmic alerts against direct patient assessment, prior knowledge of the patient, and the immediate constraints of workload and time pressure.'),
    H(' These findings are consistent with the wider literature on clinical decision support, which suggests that digital systems do not remove judgment but reshape how it is exercised in practice [[R16,R29]]. The identification of three alert response modes (overriding, deferring, and negotiating) extends binary accounts of automation bias, which contrast over-reliance with under-reliance on decision support [[N10,N4]], by showing that nurses’ responses were often conditional and professionally reasoned. Negotiation, in particular, emerged as an expression of judgment rather than indecision, consistent with conceptualisations of clinical judgment as interpretation and response grounded in knowledge of the particular patient [[N2]].')])

p = P('The findings also showed that institutional protocol')
set_segments(p, [
    U('The findings also showed that institutional protocol influenced how freely such judgment could be exercised. Documentation requirements for non-action were associated with a more defensive orientation toward alerts, whereas governance arrangements that framed alerts as one input among several were associated with a more collaborative relationship with the system.'),
    H(' These contrasts suggest that governance design may be as important as the technology itself in shaping nurses’ everyday engagement with AI.'),
    U(' Under time pressure and competing demands, participants described alert-related decision-making as faster, more intuitive, and more burdened by uncertainty [62].'),
    H(' This observation adds an experiential dimension to the literature on workload and clinical decision support by showing that uncertainty is carried not only at the moment of action, but also afterwards as an ongoing professional burden [[R63]].')])

p = P('Patient safety in AI-augmented critical care was experienced as co-produced')
set_segments(p, [
    U('Patient safety in AI-augmented critical care was experienced as co-produced through algorithmic surveillance and nursing judgment. Participants neither rejected AI as unsafe nor regarded it as sufficient on its own. Instead, they described safety as depending on whether alert outputs were meaningfully interpreted and acted upon within the context of bedside care.'),
    H(' This interpretation aligns with sociotechnical perspectives that emphasise the human work required to translate digital outputs into safe clinical action [[N3,R64]].'),
    U(' An important finding was that the perceived safety value of AI varied with nurses’ available attentional capacity.'),
    H(' AI appeared most beneficial when surveillance resources were constrained, yet those same conditions also increased vulnerability to alert fatigue [[R65]].')])

p = P('This suggests that the safety contribution')
orig = para_text(p); first = 'This suggests that the safety contribution of AI-assisted early warning is context-sensitive rather than fixed: the settings in which AI may be most useful may also be those in which its effectiveness is most vulnerable.'
assert orig.startswith(first)
set_segments(p, [H('These findings suggest that the safety contribution of AI-assisted early warning is context-sensitive rather than fixed: the settings in which AI may be most useful may also be those in which its effectiveness is most vulnerable.'), U(orig[len(first):])])

p = P('Trust, autonomy, and educational readiness emerged')
orig = para_text(p)
s4 = 'This suggests that trust in AI may be better understood as a situated practice judgment than as a stable personal trait.'
i = orig.index(s4)
set_segments(p, [U(orig[:i].rstrip(' ')),
                 H(' Taken together, these accounts suggest that trust in AI may be better understood as a situated practice judgment than as a stable personal trait, consistent with models that describe trust in automation as dynamic and calibrated through experience of a system’s reliability in a particular context [[N4]].'),
                 U(' ' + orig[i + len(s4):].lstrip(' '))])

p = P('By contrast, where alerts were framed')
orig = para_text(p)
s2 = 'These contrasts suggest that implementation strategy is a major influence on whether AI is experienced as enabling or restrictive in nursing practice. Educational readiness emerged as a further concern [68].'
i = orig.index(s2)
set_segments(p, [U(orig[:i].rstrip(' ')),
                 H(' These contrasts suggest that implementation strategy may be a major influence on whether AI is experienced as enabling or restrictive in nursing practice. Educational readiness emerged as a further concern [[R68,R60]].'),
                 U(' ' + orig[i + len(s2):].lstrip(' '))])

p = P('This study is strengthened by its multi-site design')
set_segments(p, [
    U('This study is strengthened by its multi-site design, variation in participants\' experiences and nationalities, and the use of Interpretive Description to generate practice-relevant analysis.'),
    H(' Rigour was supported through peer debriefing, participant feedback on emerging interpretations, independent coding of a subset of transcripts by a second analyst, and an audit trail.'),
    U(' Several limitations should be acknowledged. The study was confined to one regional health cluster, and its findings may not generalise directly to settings that use different AI systems, staffing models, or governance arrangements.'),
    H(' Because participation was voluntary, the sample may have favoured nurses who were more willing to reflect on AI use.'),
    U(' In addition, the study relied on narrated rather than observed practice and excluded nurses with less than one year of critical care experience, whose early encounters with AI may differ in important ways.')])
l1 = new_para_after(p, p, [H('The four sites used different AI-assisted systems with different alert types, implementation histories, training provision, and response protocols (Table 1). This heterogeneity was analytically useful, particularly for understanding how local governance shaped nurses’ engagement, but it means that the findings describe nurses’ experiences of AI-assisted early warning as implemented locally rather than the performance or effects of any single algorithm. In addition, AI-generated alerts were encountered alongside conventional monitor alarms, and participants’ accounts may not always have distinguished between the two; experiences of alert burden in particular may therefore reflect the cumulative alerting environment of the ICU rather than the AI-assisted component alone. Future studies could combine interviews with system audit data to distinguish these sources.')])
new_para_after(l1, p, [H('Participants were aged 26 to 51 years. The absence of newly qualified nurses reflects the eligibility requirement of at least one year of critical care experience, whereas the absence of nurses older than 51 years may reflect the exclusion of nurses in solely managerial roles and the voluntary recruitment approach. Workforce data were not available to establish whether this age profile was representative of critical care nurses at the participating hospitals or in Saudi Arabia more broadly, where internationally recruited nurses form a large proportion of the nursing workforce [[N11]]. Because age and career stage may shape both familiarity with digital technologies and confidence in exercising independent clinical judgment [[N9]], the experiences of late-career nurses, like those of novices, may differ from those reported here. Interviews were conducted by a nurse academic, and participants may have offered accounts they considered professionally appropriate despite assurances of confidentiality. Finally, the four themes broadly correspond to the four areas of inquiry in the interview guide. Although the interpretive content of each theme was developed through analysis (Section 2.8 and Supplementary File S2), the organisation of the findings partly reflects the domains that participants were invited to discuss.')])

p = P('This study provides qualitative evidence from the Saudi Arabian critical care context')
orig = para_text(p)
last = 'Future research should examine how different AI governance models influence nursing judgment and patient safety across critical care settings, including among nurses at earlier stages of practice.'
i = orig.index(last)
set_segments(p, [U(orig[:i].rstrip(' ')),
                 H(' Future research should examine how different AI governance models and system characteristics shape nursing judgment and patient safety across critical care settings, including among nurses at earlier and later stages of their careers, and should combine interviews with real-time observation of alert management.')])

# Table cells inherited right-to-left direction from the Normal style, which
# reversed ranges such as 36–40 on display; make every table paragraph LTR.
n_ltr = 0
for tc in body.iter(W + 'tc'):
    for pp in tc.findall(W + 'p'):
        ppr = pp.find(W + 'pPr')
        if ppr is None:
            ppr = etree.Element(W + 'pPr'); pp.insert(0, ppr)
        if ppr.find(W + 'bidi') is None:
            bd = etree.Element(W + 'bidi'); bd.set(W + 'val', '0')
            anchor = None
            for tag in ('adjustRightInd', 'snapToGrid', 'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection', 'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange'):
                anchor = ppr.find(W + tag)
                if anchor is not None: break
            (anchor.addprevious(bd) if anchor is not None else ppr.append(bd)); n_ltr += 1
print('table paragraphs set LTR:', n_ltr)
d.save('stage1.docx')
print('stage1 saved')
