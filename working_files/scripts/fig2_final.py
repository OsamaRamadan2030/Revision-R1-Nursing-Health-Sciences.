"""Figure 2 (revised): thematic map redrawn from Table 3. Undirected lines = interpretive links."""
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.family'] = 'Liberation Sans'
W, H = 6.69, 6.1
fig = plt.figure(figsize=(W, H), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
INK, LINE = '#1F2933', '#52606D'
BW, GAP, X0 = 2.0, 0.17, 0.16
TOP_Y, TOP_H = 2.35, 2.25
themes = [
 dict(title='Theme 1. Learning to read the machine', subs=['1.1 First encounters and orientation', '1.2 Developing a working relationship with the algorithm', '1.3 Navigating alert volume and frequency'], fill='#E3EEF9', edge='#3D6FA8'),
 dict(title='Theme 2. Between the alert and the bedside', subs=['2.1 Weighing the algorithm against the patient', '2.2 Alert responses and professional accountability', '2.3 Decision-making under uncertainty and time pressure'], fill='#E4F2E7', edge='#3E8A55'),
 dict(title='Theme 3. Alert, action, and the safety of the patient', subs=['3.1 AI as a safety net: enhanced surveillance and earlier recognition', '3.2 When the system misleads: false alerts and safety risk', '3.3 The human layer of safety'], fill='#FBEBDD', edge='#B5652A'),
 dict(title='Theme 4. The conditions that shape the space between alert and action', subs=['4.1 Trust as a constructed and contingent achievement', '4.2 Professional autonomy and institutional authority', '4.3 Education, support, and readiness'], fill='#EEE7F5', edge='#6B4C9A'),
]
def draw(t, x, y, w, h, tw, sw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.07', fc=t['fill'], ec=t['edge'], lw=1.2))
    title = textwrap.fill(t['title'], tw)
    ax.text(x + 0.1, y + h - 0.1, title, ha='left', va='top', fontsize=9.5, fontweight='bold', color=INK, linespacing=1.15)
    cy = y + h - 0.12 - (title.count('\n') + 1) * 0.175 - 0.1
    for s in t['subs']:
        lab, txt = s.split(' ', 1)
        wr = textwrap.fill(txt, sw)
        ax.text(x + 0.1, cy, lab, ha='left', va='top', fontsize=9, color=t['edge'], fontweight='bold')
        ax.text(x + 0.38, cy, wr, ha='left', va='top', fontsize=9, color=INK, linespacing=1.12)
        cy -= (wr.count('\n') + 1) * 0.16 + 0.08
xs = [X0 + i * (BW + GAP) for i in range(3)]
for i in range(3): draw(themes[i], xs[i], TOP_Y, BW, TOP_H, 24, 25)
B4 = (1.45, 0.15, 3.8, 1.35); draw(themes[3], *B4, 50, 60)
# banner
ax.add_patch(FancyBboxPatch((X0, 5.6), W - 2 * X0, 0.38, boxstyle='round,pad=0,rounding_size=0.06', fc='#F4F5F7', ec='#7B8794', lw=1))
ax.text(W / 2, 5.79, 'Critical care nurses’ experiences of AI-assisted early warning, clinical judgment and patient safety', ha='center', va='center', fontsize=9.3, fontweight='bold', color=INK)
def label(x, y, s):
    ax.text(x, y, s, ha='center', va='center', fontsize=9, style='italic', color='#323F4B', bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none'))
def bracket(xa, xb, yb, y0, s):
    ax.plot([xa, xa, xb, xb], [y0, yb, yb, y0], color=LINE, lw=1.3, ls=(0, (4, 2.5)))
    label((xa + xb) / 2, yb, s)
top = TOP_Y + TOP_H
bracket(xs[0] + 1.45, xs[1] + 0.55, 4.95, top, 'calibrated through experience')
bracket(xs[1] + 1.45, xs[2] + 0.55, 4.95, top, 'safety co-produced at the bedside')
bracket(xs[0] + 0.35, xs[2] + BW - 0.35, 5.3, top, 'alert burden')
cx = xs[1] + BW / 2
ax.plot([cx, cx], [B4[1] + B4[3], TOP_Y], color=LINE, lw=1.3, ls=(0, (4, 2.5)))
label(cx, (B4[1] + B4[3] + TOP_Y) / 2, 'governance shapes discretion')
fig.savefig('Figure2_final.png', dpi=300); fig.savefig('Figure2_final.pdf')
print('saved')
