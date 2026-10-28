"""Embed the curriculum, interaction code and styling in one portable HTML file."""
import json
from pathlib import Path
R=Path(__file__).parent
D=json.loads((R/'curriculum.json').read_text())
assert len(D['lessons'])==36 and all(len(l['quiz'])==2 for l in D['lessons'])
assert len(D['weeks'])==6
payload=json.dumps(D,ensure_ascii=False).replace('</','<\\/')
files={p.name:p.read_text() for p in sorted((R/'agent-build-pack').iterdir()) if p.is_file()}
source=(R/'template.html').read_text().replace('/*__CURRICULUM__*/','const DATA='+payload+';')
source=source.replace('/*__BEGINNER_CSS__*/',(R/'beginner.css').read_text())
source=source.replace('/*__BEGINNER__*/','const BUILD_FILES='+json.dumps(files,ensure_ascii=False).replace('</','<\\/')+';\n'+(R/'beginner.js').read_text())
(R/'index.html').write_text(source)
print('Built edition',D['edition'],'with',len(D['lessons']),'lessons.')
