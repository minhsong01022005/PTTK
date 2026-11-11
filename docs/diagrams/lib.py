# -*- coding: utf-8 -*-
"""Thư viện vẽ sơ đồ kiểu Visual Paradigm (xanh dương / cam) bằng Graphviz."""
import subprocess, html, os, textwrap
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
BLUE = '#7DCDF5'      # nền lớp / use case (giống mẫu đề 29)
BLUE2 = '#B9E6FA'     # nền nhạt
ORANGE = '#F6B26B'    # bảng CSDL
ORANGE2 = '#FBD9B0'
FONT = 'DejaVu Sans'

def esc(s): return html.escape(str(s), quote=False)

def render(dot, name, dpi=150):
    path = os.path.join(IMG, name + '.dot')
    open(path, 'w', encoding='utf8').write(dot)
    out = os.path.join(IMG, name + '.png')
    r = subprocess.run(['dot', '-Tpng', f'-Gdpi={dpi}', path, '-o', out], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(name + ': ' + r.stderr[:2000])
    return out

def header(extra='', rankdir='TB', nodesep='0.5', ranksep='0.7', splines='ortho'):
    return f'''digraph G {{
  graph [rankdir={rankdir}, nodesep={nodesep}, ranksep={ranksep}, splines={splines}, fontname="{FONT}", bgcolor="white", pad=0.3 {extra}];
  node [fontname="{FONT}", fontsize=11];
  edge [fontname="{FONT}", fontsize=10];
'''

def cls(name, attrs=(), methods=(), fill=BLUE, abstract=False, stereotype=None, w=None):
    """Nút lớp UML dạng bảng HTML 3 ngăn."""
    title = esc(name)
    if abstract: title = f'<I>{title}</I>'
    st = f'<FONT POINT-SIZE="9">&laquo;{esc(stereotype)}&raquo;</FONT><BR/>' if stereotype else ''
    rows = f'<TR><TD BGCOLOR="{fill}" SIDES="B" ALIGN="CENTER"><B>{st}{title}</B></TD></TR>'
    a = ''.join(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="{fill}" SIDES="">{esc(x)}</TD></TR>' for x in attrs) if attrs else f'<TR><TD BGCOLOR="{fill}" SIDES="">&nbsp;</TD></TR>'
    rows += f'<TR><TD BGCOLOR="{fill}" SIDES="B" ALIGN="LEFT" CELLPADDING="0"><TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2">{a}</TABLE></TD></TR>'
    if methods is not None:
        m = ''.join(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{esc(x)}</TD></TR>' for x in methods) if methods else '<TR><TD>&nbsp;</TD></TR>'
        rows += f'<TR><TD BGCOLOR="{fill}" ALIGN="LEFT" CELLPADDING="0"><TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2">{m}</TABLE></TD></TR>'
    return f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" BGCOLOR="{fill}">{rows}</TABLE>>'

def node(id_, label, extra=''):
    return f'  {id_} [shape=plaintext, margin=0, label={label}{(", " + extra) if extra else ""}];\n'
