"""Derive the clean copy from the highlighted file.

Removes yellow highlighting and only the bold that was added to mark revisions
(written as <w:b w:val="1"/>); the author's own bold (<w:b/>) is preserved.
"""
import sys, zipfile, re
from lxml import etree
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
src, out = sys.argv[1], sys.argv[2]
TARGET = re.compile(r'^word/(document|footnotes|endnotes|header\d*|footer\d*)\.xml$')
nh = nb = 0
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if TARGET.match(item.filename):
            root = etree.fromstring(data)
            for rpr in root.iter(W + 'rPr'):
                hls = rpr.findall(W + 'highlight')
                if not hls: continue
                for h in hls: rpr.remove(h); nh += 1
                for tag in ('b', 'bCs'):
                    for el in rpr.findall(W + tag):
                        if el.get(W + 'val') == '1':
                            rpr.remove(el); nb += 1
            data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        zout.writestr(item, data)
print(f'{out}: removed {nh} highlights, {nb} revision-bold marks')
