"""Helpers for editing the manuscript in place while preserving its template."""
import copy, re
from lxml import etree
from docx.oxml.ns import qn

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XMLSP = '{http://www.w3.org/XML/1998/namespace}space'

# CT_RPr child order (subset sufficient here)
RPR_ORDER = ['rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike',
             'outline', 'shadow', 'emboss', 'imprint', 'noProof', 'snapToGrid', 'vanish', 'webHidden',
             'color', 'spacing', 'w', 'kern', 'position', 'sz', 'szCs', 'highlight', 'u', 'effect',
             'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs', 'em', 'lang', 'eastAsianLayout',
             'specVanish', 'oMath']


def _rpr_set(rpr, tag, attrs=None):
    """Insert or replace child <w:tag> in rPr respecting schema order."""
    for el in rpr.findall(W + tag):
        rpr.remove(el)
    el = etree.SubElement(rpr, W + tag)
    for k, v in (attrs or {}).items():
        el.set(W + k, v)
    # reorder
    kids = list(rpr)
    for k in kids:
        rpr.remove(k)
    kids.sort(key=lambda e: RPR_ORDER.index(etree.QName(e).localname)
              if etree.QName(e).localname in RPR_ORDER else 999)
    for k in kids:
        rpr.append(k)
    return el


def _rpr_del(rpr, tag):
    for el in rpr.findall(W + tag):
        rpr.remove(el)


def make_run(text, base_rpr=None, hl=False, bold=None, italic=None, size=None):
    """Build a <w:r>.

    hl=True marks a revision: yellow highlight plus bold. The bold added for marking
    is written as <w:b w:val="1"/> so the clean-copy script can tell it apart from
    the author's own bold (<w:b/>), which it must keep.
    bold=True means intrinsic bold (kept in clean copy); bold=False removes bold.
    """
    r = etree.Element(W + 'r')
    rpr = copy.deepcopy(base_rpr) if base_rpr is not None else etree.Element(W + 'rPr')
    rpr.tag = W + 'rPr'
    _rpr_del(rpr, 'highlight')
    if bold is True:
        _rpr_set(rpr, 'b'); _rpr_set(rpr, 'bCs')
    elif bold is False:
        _rpr_del(rpr, 'b'); _rpr_del(rpr, 'bCs')
    if italic is True:
        _rpr_set(rpr, 'i'); _rpr_set(rpr, 'iCs')
    elif italic is False:
        _rpr_del(rpr, 'i'); _rpr_del(rpr, 'iCs')
    if size:
        _rpr_set(rpr, 'sz', {'val': str(size)}); _rpr_set(rpr, 'szCs', {'val': str(size)})
    if hl:
        has_b = any(el.get(W + 'val', 'true').lower() not in ('0', 'false') for el in rpr.findall(W + 'b'))
        if not has_b:
            _rpr_set(rpr, 'b', {'val': '1'}); _rpr_set(rpr, 'bCs', {'val': '1'})
        _rpr_set(rpr, 'highlight', {'val': 'yellow'})
    if len(rpr):
        r.append(rpr)
    t = etree.SubElement(r, W + 't')
    t.text = text
    t.set(XMLSP, 'preserve')
    return r


def para_text(p_el):
    return ''.join(t.text or '' for t in p_el.iter(W + 't'))


def first_plain_rpr(p_el):
    """rPr of the first non-bold run with text (body formatting)."""
    for r in p_el.findall(W + 'r'):
        if r.find(W + 't') is None:
            continue
        rpr = r.find(W + 'rPr')
        if rpr is None:
            return None
        if rpr.find(W + 'b') is None:
            return rpr
    r = p_el.find(W + 'r')
    return r.find(W + 'rPr') if r is not None else None


def clear_runs(p_el, keep_first_n=0):
    runs = [c for c in p_el if etree.QName(c).localname in ('r', 'hyperlink', 'proofErr', 'bookmarkStart', 'bookmarkEnd')]
    kept = 0
    for c in runs:
        if etree.QName(c).localname == 'r' and kept < keep_first_n:
            kept += 1
            continue
        p_el.remove(c)


def set_segments(p_el, segments, base_rpr=None, keep_first_n=0, check_original=True):
    """Replace paragraph content by segments [(text, hl, opts)].

    Unhighlighted segments must reproduce original wording: we assert that each one
    occurs in the original paragraph text (guards against silent drift).
    """
    orig = para_text(p_el)
    if base_rpr is None:
        base_rpr = first_plain_rpr(p_el)
    base_rpr = copy.deepcopy(base_rpr) if base_rpr is not None else None
    if check_original:
        for seg in segments:
            text, hl = seg[0], seg[1]
            if not hl and text.strip() and text not in orig:
                raise AssertionError('Unchanged segment not found in original:\n  ' + text[:120] + '\n  ORIG: ' + orig[:200])
    clear_runs(p_el, keep_first_n)
    for seg in segments:
        text, hl = seg[0], seg[1]
        opts = seg[2] if len(seg) > 2 else {}
        p_el.append(make_run(text, base_rpr, hl=hl, **opts))
    return p_el


def new_para_after(anchor_el, template_p_el, segments, base_rpr=None):
    """Insert a new paragraph after anchor, copying pPr from template paragraph."""
    p = etree.Element(W + 'p')
    ppr = template_p_el.find(W + 'pPr')
    if ppr is not None:
        p.append(copy.deepcopy(ppr))
    if base_rpr is None:
        base_rpr = first_plain_rpr(template_p_el)
    for seg in segments:
        text, hl = seg[0], seg[1]
        opts = seg[2] if len(seg) > 2 else {}
        p.append(make_run(text, base_rpr, hl=hl, **opts))
    anchor_el.addnext(p)
    return p


def unlink_fields(body):
    """Convert complex fields (Mendeley citations/bibliography) to static text.

    merge_runs may have coalesced fldChar/instrText into text runs, so work at the
    element level: drop every fldChar and instrText, keep the displayed w:t, then
    remove runs left with no content.
    """
    n = 0
    for el in list(body.iter(W + 'fldChar')):
        if el.get(W + 'fldCharType') == 'begin':
            n += 1
        el.getparent().remove(el)
    for el in list(body.iter(W + 'instrText')):
        el.getparent().remove(el)
    for r in list(body.iter(W + 'r')):
        if all(etree.QName(c).localname == 'rPr' for c in r):
            r.getparent().remove(r)
    return n
