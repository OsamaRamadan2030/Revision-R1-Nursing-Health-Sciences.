import re, sys, zipfile, docx
sys.path.insert(0, '/tmp/rt2')
from locate import loc
from lib import *
def P(f): return [para_text(p) for p in docx.Document(f).element.body.iter(W + 'p')]
problems = []
def bad(msg): problems.append(msg); print('PROBLEM:', msg)

HL, CL = 'Manuscript_Revised_Highlighted.docx', 'Manuscript_Revised_Clean.docx'
hl, cl = P(HL), P(CL)
if hl != cl: bad('clean and highlighted manuscript text differ')
for f in (CL, 'Title_Page_Revised_Clean.docx', 'S1_Supplementary_Interview_Guide_Revised_Clean.docx'):
    with zipfile.ZipFile(f) as z:
        if b'w:highlight' in z.read('word/document.xml'): bad(f + ' still contains highlighting')
if P('Title_Page_Revised_Highlighted.docx') != P('Title_Page_Revised_Clean.docx'): bad('title page clean/highlighted differ')
if P('S1_Supplementary_Interview_Guide_Revised_Highlighted.docx') != P('S1_Supplementary_Interview_Guide_Revised_Clean.docx'): bad('S1 clean/highlighted differ')

# highlighted-character map of the highlighted manuscript
hdoc = docx.Document(HL)
chars = []  # (char, highlighted)
for p in hdoc.element.body.iter(W + 'p'):
    for r in p.iter(W + 'r'):
        rpr = r.find(W + 'rPr'); h = rpr is not None and rpr.find(W + 'highlight') is not None
        for t in r.findall(W + 't'):
            for ch in (t.text or ''): chars.append((ch, h))
    chars.append(('\n', False))
htext = ''.join(c for c, _ in chars)

L = docx.Document('Response_to_Editor_and_Reviewers.docx').paragraphs
other = '\n'.join(P('Title_Page_Revised_Clean.docx') + P('S1_Supplementary_Interview_Guide_Revised_Clean.docx'))
n = 0
for i, p in enumerate(L):
    t = p.text
    if not (t.startswith('“') and t.endswith('”')): continue
    q = t[1:-1]; n += 1
    where = L[i - 1].text
    if q in htext:
        k = htext.index(q)
        unhl = [c for c, h in chars[k:k + len(q)] if not h and c.strip()]
        frac = len(unhl) / max(1, len([c for c in q if c.strip()]))
        if frac > 0.02: bad(f'quote {n} not (fully) highlighted in manuscript ({frac:.0%} unhighlighted): {q[:70]}')
        m = re.search(r'(pp?\. [\d–]+, lines? [\d–]+)', where)
        if m:
            words = q.split()
            got = loc(' '.join(words[:10]), ' '.join(words[-4:]))
            if got != m.group(1): bad(f'quote {n} location: letter says {m.group(1)}, file gives {got}')
    elif q not in other:
        bad(f'quote {n} not found in any revised file: {q[:80]}')
print('letter quotes checked:', n)

# reviewer comments verbatim
src = '\n'.join(P('comments.docx'))
src_n = re.sub(r'\s+', '', src)
for p in L:
    t = p.text
    m = re.match(r'^(Comment [E\d.]+|Handling editor\.|General comment\.|Closing remark\.)\s+(.*)$', t)
    if not m: continue
    for part in t[len(m.group(1)):].strip().split(' … '):
        if re.sub(r'\s+', '', part.strip()) not in src_n: bad(f'comment not verbatim: {m.group(1)} {part[:80]}')

# citations: every number 1..N cited, first-citation order ascending
refs_i = next(i for i, t in enumerate(cl) if t.strip() == 'References')
body = '\n'.join(cl[:refs_i]); reflist = [t for t in cl[refs_i + 1:] if re.match(r'^\d+\. ', t)]
N = len(reflist)
nums = []
for m in re.finditer(r'\[(\d+(?:\s*[,–]\s*\d+)*)\]', body):
    for part in m.group(1).split(','):
        part = part.strip()
        if '–' in part:
            a, b = map(int, part.split('–')); nums += list(range(a, b + 1))
        else: nums.append(int(part))
first = []
for x in nums:
    if x not in first: first.append(x)
if sorted(first) != list(range(1, N + 1)): bad(f'cited set != 1..{N}: missing {set(range(1,N+1))-set(first)}')
if first != sorted(first): bad('references not numbered in order of first citation')
if [int(r.split('.')[0]) for r in reflist] != list(range(1, N + 1)): bad('reference list numbering broken')
print('references:', N, '; in-text citation order OK' if first == sorted(first) else '')

# tables / figures cited in order and present
for kind in ('Table', 'Figure'):
    mentions = [int(x) for x in re.findall(kind + r' (\d)', body)]
    seen = []
    for x in mentions:
        if x not in seen: seen.append(x)
    if seen != sorted(seen): bad(f'{kind}s first cited out of order: {seen}')
    print(kind, 'first-citation order:', seen)

# leaked letter phrasing
for t in cl:
    for q in ('as suggested', 'the reviewer', 'we have added', 'we have revised', 'in response to the', 'as requested', 'thank you'):
        if q in t.lower(): bad(f'leaked phrasing "{q}": {t[:80]}')

# placeholders
for f in ('Manuscript_Revised_Clean.docx', 'Title_Page_Revised_Clean.docx', 'S2_Supplementary_Analytic_Trail.docx', 'S3_COREQ_Checklist.docx', 'Response_to_Editor_and_Reviewers.docx', 'S1_Supplementary_Interview_Guide_Revised_Clean.docx'):
    print(f'{f}: {sum(t.count("[AUTHOR:") for t in P(f))} placeholders')
print('\nTOTAL PROBLEMS:', len(problems))
