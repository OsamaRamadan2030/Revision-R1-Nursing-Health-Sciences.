import re, copy, json
import docx
from lib import *

d = docx.Document('stage1.docx')
body = d.element.body
paras = list(body.iter(W + 'p'))

# ---- old reference list
ref_head = [p for p in paras if para_text(p).strip() == 'References'][0]
old_refs = {}
ref_paras = []
nxt = ref_head.getnext()
while nxt is not None and nxt.tag == W + 'p':
    t = para_text(nxt)
    m = re.match(r'^(\d+)\.\s+(.*)$', t, re.S)
    if m:
        old_refs['R' + m.group(1)] = m.group(2).strip()
        ref_paras.append(nxt)
    elif t.strip():
        break
    else:
        ref_paras.append(nxt)
    nxt = nxt.getnext()
assert len(old_refs) == 69, len(old_refs)
tmpl_ref = ref_paras[1]
tmpl_rpr = copy.deepcopy([r for r in tmpl_ref.findall(W + 'r') if r.find(W + 't') is not None][0].find(W + 'rPr'))

OLDMAP = {f'{i}': f'R{i}' for i in range(1, 70)}
OLDMAP['35'] = 'R12'; OLDMAP['36'] = 'R26'
REMOVED = {'R35', 'R36', 'R42'}

fixed = dict(old_refs)
changed = set()
def fix(k, new):
    fixed[k] = new; changed.add(k)
fix('R17', old_refs['R17'].replace('2025;Volume 18:', '2025;18:'))
fix('R41', old_refs['R41'].replace(';WGROUP:STRING:PUBLICATION', ''))
fix('R50', 'Cope DG. Methods and meanings: credibility and trustworthiness of qualitative research. Oncol Nurs Forum. 2014;41:89–91. https://doi.org/10.1188/14.ONF.89-91.')
fix('R54', re.sub(r'Criteria for Assessing and Ensuring the Trustworthiness in Criteria.*?QUALITATIVE RESEARCH\.', 'Criteria for assessing and ensuring the trustworthiness in qualitative research.', old_refs['R54']))
fix('R57', old_refs['R57'].replace('/TABLES/3', ''))
fix('R63', old_refs['R63'].replace('<scp>', '').replace('</scp>', ''))
for k in ('R54',):
    assert 'CRITERIA' not in fixed[k], fixed[k]

NEW = {
 'N1': 'Kingdom of Saudi Arabia. Saudi Vision 2030: Health Sector Transformation Program [Internet]. Riyadh: Council of Economic and Development Affairs; [cited 2026 Oct 1]. Available from: https://www.vision2030.gov.sa/en/explore/programs/health-sector-transformation-program.',
 'N2': 'Tanner CA. Thinking like a nurse: a research-based model of clinical judgment in nursing. J Nurs Educ. 2006;45:204–11. https://doi.org/10.3928/01484834-20060601-04.',
 'N3': 'Sittig DF, Singh H. A new sociotechnical model for studying health information technology in complex adaptive healthcare systems. Qual Saf Health Care. 2010;19 Suppl 3:i68–74. https://doi.org/10.1136/qshc.2010.042085.',
 'N4': 'Lee JD, See KA. Trust in automation: designing for appropriate reliance. Hum Factors. 2004;46:50–80. https://doi.org/10.1518/hfes.46.1.50_30392.',
 'N5': 'Braun V, Clarke V. Thematic Analysis: A Practical Guide. London: SAGE; 2022.',
 'N6': 'Holden RJ, Karsh B-T. The technology acceptance model: its past and its future in health care. J Biomed Inform. 2010;43:159–72. https://doi.org/10.1016/j.jbi.2009.07.002.',
 'N7': 'Greenhalgh T, Wherton J, Papoutsi C, Lynch J, Hughes G, A’Court C, et al. Beyond adoption: a new framework for theorizing and evaluating nonadoption, abandonment, and challenges to the scale-up, spread, and sustainability of health and care technologies. J Med Internet Res. 2017;19:e367. https://doi.org/10.2196/jmir.8775.',
 'N8': 'Almutairi AF, McCarthy A, Gardner GE. Understanding cultural competence in a multicultural nursing workforce: registered nurses’ experience in Saudi Arabia. J Transcult Nurs. 2015;26:16–23. https://doi.org/10.1177/1043659614523992.',
 'N9': 'Benner P. From Novice to Expert: Excellence and Power in Clinical Nursing Practice. Menlo Park, CA: Addison-Wesley; 1984.',
 'N10': 'Goddard K, Roudsari A, Wyatt JC. Automation bias: a systematic review of frequency, effect mediators, and mitigators. J Am Med Inform Assoc. 2012;19:121–7. https://doi.org/10.1136/amiajnl-2011-000089.',
 'N11': 'Alluhidan M, Tashkandi N, Alblowi F, Omer T, Alghaith T, Alghodaier H, et al. Challenges and policy opportunities in nursing in Saudi Arabia. Hum Resour Health. 2020;18:98. https://doi.org/10.1186/s12960-020-00535-2.',
}
ALL = {**fixed, **NEW}

NUM_RE = re.compile(r'\[(\d+(?:\s*[,–-]\s*\d+)*)\]')
TOK_RE = re.compile(r'\[\[([RN]\d+(?:,[RN]\d+)*)\]\]')

def expand(s):
    out = []
    for part in re.split(r'\s*,\s*', s):
        if re.search(r'[–-]', part):
            a, b = re.split(r'\s*[–-]\s*', part)
            out += [str(x) for x in range(int(a), int(b) + 1)]
        else:
            out.append(part.strip())
    return out

# pass 1: numeric -> tokens (in document body excluding reference list)
body_paras = [p for p in body.iter(W + 'p') if p not in ref_paras and p is not ref_head]
for p in body_paras:
    for t in p.iter(W + 't'):
        if t.text and NUM_RE.search(t.text):
            t.text = NUM_RE.sub(lambda m: '[[' + ','.join(OLDMAP[x] for x in expand(m.group(1))) + ']]', t.text)

# pass 2: order of first appearance
order = []
for p in body_paras:
    for t in p.iter(W + 't'):
        for m in TOK_RE.finditer(t.text or ''):
            for k in m.group(1).split(','):
                if k not in order:
                    order.append(k)
num = {k: i + 1 for i, k in enumerate(order)}

def fmt(keys):
    ns = sorted(set(num[k] for k in keys))
    out, i = [], 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out.append(f'{ns[i]}–{ns[j]}' if j - i >= 2 else ', '.join(str(x) for x in ns[i:j + 1]))
        i = j + 1
    return '[' + ', '.join(out) + ']'

for p in body_paras:
    for t in p.iter(W + 't'):
        if t.text and '[[' in t.text:
            t.text = TOK_RE.sub(lambda m: fmt(m.group(1).split(',')), t.text)

# checks
missing = [k for k in ALL if k not in num and k not in REMOVED]
print('uncited refs:', missing)
assert not [k for k in order if k in REMOVED], 'removed ref still cited'
assert all(k in ALL for k in order)

# pass 3: rebuild list
for p in ref_paras:
    p.getparent().remove(p)
anchor = ref_head
for k in order:
    np_ = etree.Element(W + 'p')
    if tmpl_ref.find(W + 'pPr') is not None:
        np_.append(copy.deepcopy(tmpl_ref.find(W + 'pPr')))
    hl = k.startswith('N') or k in changed
    np_.append(make_run(f'{num[k]}. {ALL[k]}', tmpl_rpr, hl=hl))
    anchor.addnext(np_); anchor = np_

json.dump({'order': order, 'num': num}, open('refmap.json', 'w'), indent=1)
print('total refs:', len(order))
print('new numbers:', {k: num[k] for k in order if k.startswith('N')})
for t in body.iter(W + 't'):
    if t.text and (t.text != t.text.strip()):
        t.set(XMLSP, 'preserve')
d.save('Manuscript_Revised_Highlighted.docx')
print('saved')
