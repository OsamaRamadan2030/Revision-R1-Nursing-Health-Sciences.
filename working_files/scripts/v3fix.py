import re, copy, docx
from lib import *
from lib import _rpr_set
def ts(p): return [t for t in p.iter(W + 't')]
def replace(p, old, new):
    """Replace text spanning any runs; new text goes into the first touched w:t (keeps its formatting)."""
    T = ts(p); full = ''.join(t.text or '' for t in T)
    i = full.find(old); assert i >= 0, ('not found', old[:70])
    j = i + len(old); pos = 0; first = True
    for t in T:
        s = t.text or ''; a, b = pos, pos + len(s); pos = b
        if b <= i or a >= j: continue
        lo, hi = max(i, a) - a, min(j, b) - a
        t.text = s[:lo] + (new if first else '') + s[hi:]; first = False
        t.set(XMLSP, 'preserve')
def P(body, prefix):
    h = [p for p in body.iter(W + 'p') if para_text(p).startswith(prefix)]
    assert len(h) == 1, (prefix, len(h)); return h[0]
def find(body, sub):
    h = [p for p in body.iter(W + 'p') if sub in para_text(p)]
    assert len(h) == 1, (sub, len(h)); return h[0]

# ---------------- manuscript (blinding + Figure 2)
d = docx.Document('v3/ms.docx'); b = d.element.body
replace(find(b, 'confidentiality agreement with Jouf University'), 'with Jouf University', 'with XXX University')
replace(find(b, 'Institutional Review Board of Jouf University'), 'of Jouf University (approval No. 7066, 1 January 2026)', 'of XXX University (reference number withheld for blinded review)')
replace(find(b, 'Jouf University’s research data'), 'Jouf University’s', 'XXX University’s')
replace(find(b, 'The authors’ related study examines automation bias'), 'The authors’ related study examines', 'A related study examines')
replace(find(b, 'used in the authors’ related study'), 'the authors’ related study', 'a related study')
replace(find(b, 'The authors’ related study specifically examines'), 'The authors’ related study specifically examines', 'A related study specifically examines')
assert 'Jouf' not in '\n'.join(para_text(p) for p in b.iter(W + 'p') if not re.match(r'^\d+\. ', para_text(p)))
# Figure 2 image
img_p = [p for p in b.iter(W + 'p') if list(p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))][-1]
rid = list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
d.part.related_parts[rid]._blob = open('Figure2_final.png', 'rb').read()
for ext in list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')) + list(img_p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}ext')):
    if ext.get('cx'): ext.set('cy', str(int(int(ext.get('cx')) * 6.1 / 6.69)))
leg = P(b, 'Figure 2. Thematic map')
rpr = [r for r in leg.findall(W + 'r') if r.find(W + 't') is not None][-1].find(W + 'rPr')
leg.append(make_run(' Each theme is shown with its three subthemes; dashed lines indicate interpretive relationships described in the text, not causal pathways. The figure was drawn by the authors using AI-assisted plotting code generated from the authors’ themes and subthemes (Table 3).', rpr, hl=True))
for t in b.iter(W + 't'):
    if t.text and t.text != t.text.strip(): t.set(XMLSP, 'preserve')
d.save('FINAL_Manuscript_Highlighted.docx')

# ---------------- title page
d = docx.Document('v3/tp.docx'); b = d.element.body
ack = find(b, 'Grammarly and QuillBot')
replace(ack, 'Figure 1 and 2 was created by the authors without the use of artificial intelligence tools.', 'Figure 1 was created by the authors without the use of artificial intelligence tools. During revision, AI assistance was used to support drafting and editing of revised text, consistency checking, and generation of the plotting code for Figure 2; the authors reviewed and verified all content and take full responsibility for it.')
eth = find(b, 'Jouf University Institutional Review Board')
replace(eth, 'Jouf University Institutional Review Board', 'Jouf University Institutional Review Board (approval No. 7066, 1 January 2026)')
d.save('FINAL_Title_Page_Highlighted.docx')

# ---------------- letter
d = docx.Document('v3/letter.docx'); b = d.element.body
e3 = find(b, 'The title-page Acknowledgments now give a consistent account')
replace(e3, para_text(e3)[len('Response: '):] if para_text(e3).startswith('Response: ') else para_text(e3),
 'AI tools were not used to collect or transcribe interviews, code the data, or develop the study findings. The title-page Acknowledgments report the use of Grammarly and QuillBot for language editing and state that, during revision, AI assistance supported drafting and editing of revised text, consistency checking, and generation of the plotting code for Figure 2. No recordings or transcripts were shared, participant quotations were not altered, and the authors verified all content. The Figure 1 legend states that it was created without AI tools; the Figure 2 legend discloses the plotting-code assistance.')
f2 = find(b, 'Figure 2 has been redrawn as four readable theme blocks')
replace(f2, para_text(f2)[para_text(f2).index('Figure 2 has been redrawn'):],
 'Figure 2 has been redrawn at print resolution. Decorative icons and background elements were removed, each theme is shown as a single block listing its three subthemes, and all labels match Table 3, including the renamed subtheme 2.2. All text is at least 9 pt at the 17 cm print width. Dashed lines mark the interpretive links described in the text, and the legend states that they are not causal pathways.')
d.save('FINAL_Response_to_Editor_and_Reviewers.docx')

# ---------------- S3 item 28
d = docx.Document('v3/s3.docx'); b = d.element.body
replace(find(b, 'Member checking with six purposively selected participants.'), 'Member checking with six purposively selected participants.', 'Participant reflection: six purposively selected participants reviewed summary accounts of the emerging themes.')
d.save('FINAL_S3_COREQ_Checklist.docx')
print('done')
