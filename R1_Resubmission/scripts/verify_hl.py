"""Check that the highlighted manuscript marks every change.

1. Every NON-highlighted run must reproduce original wording (citation numbers normalised).
2. Participant quotations (text before the attribution) must be identical to the original.
3. Report original sentences that no longer appear (deletions) so the letter can cover them.
"""
import re, sys, docx
from lib import *
CIT = re.compile(r'\[\d+(?:\s*[,–-]\s*\d+)*\]')
def norm(s): return re.sub(r'\s+', ' ', CIT.sub('[#]', s)).strip()
orig = docx.Document('ms.docx'); rev = docx.Document(sys.argv[1] if len(sys.argv) > 1 else 'Manuscript_Revised_Highlighted.docx')
def paras(d):
    return [p for p in d.element.body.iter(W + 'p')]
otext = norm(' '.join(para_text(p) for p in paras(orig)))
bad = []
for p in paras(rev):
    plain = ''
    for r in p.iter(W + 'r'):
        rpr = r.find(W + 'rPr'); hl = rpr is not None and rpr.find(W + 'highlight') is not None
        t = ''.join(x.text or '' for x in r.findall(W + 't'))
        if hl:
            if plain.strip(): 
                if norm(plain) not in otext: bad.append(plain)
            plain = ''
        else:
            plain += t
    if plain.strip() and norm(plain) not in otext: bad.append(plain)
# references section is rebuilt: ignore lines starting with a number + period
bad = [b for b in bad if not re.match(r'^\d+\. ', b.strip())]
# known, letter-documented deletion: duplicated sentence 'Critical care experience ranged from 2 to 23 years.'
bad = [b for b in bad if norm(b.replace('(n = 2). Most', '(n = 2). Critical care experience ranged from 2 to 23 years. Most')) not in otext]
print('UNHIGHLIGHTED TEXT NOT IN ORIGINAL:', len(bad))
for b in bad: print('  >>', b[:220])
# quotations
def quotes(d):
    out = []
    for p in paras(d):
        t = para_text(p)
        m = re.match(r'^(.*)\((P\d\d), (female|male), [^)]*\)\s*$', t, re.S)
        if m: out.append((m.group(2), m.group(1).strip()))
    return out
qo, qr = quotes(orig), quotes(rev)
print('quotations: original', len(qo), 'revised', len(qr), 'identical:', qo == qr)
for a, b in zip(qo, qr):
    if a != b: print('  QUOTE CHANGED', a[0])
# deletions: original sentences (>6 words) absent from revised
rtext = norm(' '.join(para_text(p) for p in paras(rev)))
otxt_list = [para_text(p) for p in paras(orig)]
ref_start = next(i for i, t in enumerate(otxt_list) if t.strip() == 'References')
dels = []
for t in otxt_list[:ref_start]:
    for s in re.split(r'(?<=[.?!])\s+(?=[A-Z“"])', t):
        if len(s.split()) > 6 and norm(s) not in rtext: dels.append(s)
print('ORIGINAL SENTENCES REMOVED OR REWRITTEN:', len(dels))
for s in dels: print('  --', s[:200])
