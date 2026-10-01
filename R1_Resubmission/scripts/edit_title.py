import docx
from lib import *
d = docx.Document('title_merged.docx'); body = d.element.body
def P(prefix):
    hits = [p for p in body.iter(W + 'p') if para_text(p).strip().startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits)); return hits[0]
def H(t, **o): return (t, True, o)
def U(t, **o): return (t, False, o)

p = P("Between Alert and Action: Nurses' Experiences")
t = para_text(p); assert t.endswith('Care.')
set_segments(p, [U(t[:-1]), H('')])  # drop trailing full stop to match manuscript title
# (empty highlighted run carries no text; the deletion is explained in the letter)
p.remove(p.findall(W + 'r')[-1])

ack = P('The authors gratefully acknowledge the nurses')
AI = ('The authors used Grammarly and QuillBot solely for grammar, spelling, and readability edits to author-written text. '
      'These tools were not used for study design or conduct, data analysis, interpretation, or reference generation. '
      'Only de-identified manuscript text was processed; no recordings or interview transcripts were uploaded, and participant '
      'quotations remained unchanged. The authors reviewed all edits for accuracy and fidelity to the study data and sources, '
      'approved the final manuscript, and retain full responsibility for its content.')
p_ai = new_para_after(ack, ack, [H(AI)])
p_fig = new_para_after(p_ai, ack, [H('No artificial intelligence tools were used to create or enhance Figures 1 and 2.')])
new_para_after(p_fig, ack, [H('[AUTHOR: if an AI assistant was used to help prepare this revision, for example to draft revised text or the response letter, journal policy requires that use to be disclosed here; see Final_Audit_Report.md, item B0. Delete this note once resolved.]')])

eth = P('Ethical approval was obtained from the Jouf University Institutional Review Board')
t = para_text(eth)
k = 'Ethical approval was obtained from the Jouf University Institutional Review Board'
i = t.index(k) + len(k)
set_segments(eth, [U(t[:i]), H(' (approval no. [AUTHOR: insert IRB reference number and approval date])'), U(t[i:])])

g = P('Ghada Elsaid Ali Elsayed:')
set_segments(g, [H(' Conceptualisation (supporting), Investigation, Validation, Supervision, Writing – review & editing.')], keep_first_n=1)
r = P('Reda Samy:')
set_segments(r, [H(' Formal analysis (supporting), Validation, Writing – review & editing.')], keep_first_n=1)

for t in body.iter(W + 't'):
    if t.text and t.text != t.text.strip(): t.set(XMLSP, 'preserve')
d.save('Title_Page_Revised_Highlighted.docx'); print('ok')
