import re, sys, json
pages = open('/tmp/rt2/hl.txt').read().split('\f')
lines = []  # (page, lineno, text)
for pi, pg in enumerate(pages):
    for ln in pg.split('\n'):
        m = re.match(r'\s*(\d+)\s{2,}(.*)', ln)
        if m: lines.append((pi + 1, int(m.group(1)), m.group(2)))
flat = ''; idx = []
for i, (p, n, t) in enumerate(lines):
    t = re.sub(r'\s+', ' ', t.strip())
    for ch in t + ' ':
        flat += ch; idx.append(i)
def norm(s): return re.sub(r'\s+', ' ', s)
def loc(start, end=None):
    k = flat.find(norm(start))
    if k < 0:
        # handle hyphenation breaks
        k = flat.replace('- ', '-').find(norm(start))
        if k < 0: return None
    a = lines[idx[k]]
    if end:
        e = flat.find(norm(end), k)
        b = lines[idx[e + len(norm(end)) - 1]] if e >= 0 else a
    else:
        b = a
    pg = f'p. {a[0]}' if a[0] == b[0] else f'pp. {a[0]}–{b[0]}'
    ln = f'line {a[1]}' if a[1] == b[1] else f'lines {a[1]}–{b[1]}'
    return f'{pg}, {ln}'
if __name__ == '__main__':
    for s in sys.argv[1:]:
        st, _, en = s.partition('||')
        print(s[:40], '->', loc(st, en or None))
