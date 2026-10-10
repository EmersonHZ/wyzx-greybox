#!/usr/bin/env python3
"""把 src.html 里的 /*__MAPDATA__*/ 占位替换成 mapdata.js，输出 index.html。
用法：python3 build.py（在 demo/ 目录下）"""
import pathlib, re, subprocess, sys
here = pathlib.Path(__file__).parent
src = (here / 'src.html').read_text(encoding='utf-8')
md = (here / 'mapdata.js').read_text(encoding='utf-8')
assert '/*__MAPDATA__*/' in src, 'src.html 缺占位符'
out = src.replace('/*__MAPDATA__*/', md)
(here / 'index.html').write_text(out, encoding='utf-8')
scripts = re.findall(r'<script>(.*?)</script>', out, re.S)
(here / '.check.js').write_text('\n'.join(scripts), encoding='utf-8')
r = subprocess.run(['node', '--check', str(here / '.check.js')], capture_output=True, text=True)
(here / '.check.js').unlink(missing_ok=True)
if r.returncode:
    print(r.stderr); sys.exit(1)
print('index.html', len(out.encode('utf-8')), 'bytes · syntax ok')
