import docx, re
from lib import *
d = docx.Document('s1_merged.docx'); body = d.element.body
def H(t, **o): return (t, True, o)
def U(t, **o): return (t, False, o)
labels = {
 '(Theme 1)': '(Area of inquiry 1; Objective 1)',
 '(Theme 2)': '(Area of inquiry 2; Objective 2)',
 '(Theme 3)': '(Area of inquiry 3; Objective 3)',
 '(Theme 4)': '(Area of inquiry 4; Objective 4)',
}
n = 0
for p in body.iter(W + 'p'):
    t = para_text(p)
    for k, v in labels.items():
        if k in t:
            i = t.index(k)
            set_segments(p, [U(t[:i]), H(v), U(t[i + len(k):])]); n += 1
print('labels replaced', n)
# note on section labels, inserted before the Opening Statement heading
op = [p for p in body.iter(W + 'p') if para_text(p).startswith('Opening Statement')][0]
tmpl = [p for p in body.iter(W + 'p') if para_text(p).startswith('These opening questions aim')][0]
note = etree.Element(W + 'p'); note.append(copy.deepcopy(tmpl.find(W + 'pPr')))
base = first_plain_rpr(tmpl)
note.append(make_run('Note on section labels. ', base, hl=True, bold=True))
note.append(make_run('During data collection, Sections B1–B4 were labelled by area of inquiry only; each area corresponds to one study objective and was derived from the orienting conceptual framework (manuscript Figure 1). In the version of this file submitted with the original manuscript, the sentence introducing each section also cross-referenced the corresponding final theme. These cross-references were added after analysis, for presentation only, and have now been replaced by the area-of-inquiry labels used during data collection. The themes reported in the manuscript were developed through reflexive thematic analysis and were not predefined; Supplementary File S2 traces how the areas of inquiry, initial codes, and final themes relate.', base, hl=True))
op.addprevious(note)
for t in body.iter(W + 't'):
    if t.text and t.text != t.text.strip(): t.set(XMLSP, 'preserve')
d.save('S1_Supplementary_Interview_Guide_Revised_Highlighted.docx'); print('ok')
