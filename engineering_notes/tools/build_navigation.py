"""Regenerate shared navigation, preserving separate engineering/system-design tracks."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
groups=json.loads((ROOT/'topics.json').read_text())
for p in [*ROOT.glob('*.html'),ROOT.parent/'engineering_notes.html']:
 s=p.read_text();prefix='engineering_notes/' if p.parent==ROOT.parent else ''
 own=next((g for g in groups if any(t['file']==p.name for t in g['topics'])),None)
 area=own.get('area','engineering') if own else 'engineering'
 visible=[g for g in groups if g.get('area','engineering')==area]
 label='System design' if area=='system-design' else 'General tech'
 nav='<nav aria-label="Topics"><div class="navigation-heading">'+label+'</div>'
 for g in visible:
  current=any(t['file']==p.name for t in g['topics']);n=len(g['topics'])
  nav+='<details class="nav-group"'+(' open' if current else '')+'><summary><span class="nav-group-title">'+escape(g['group'])+'</span><span class="nav-group-count" aria-label="'+str(n)+' topics">'+str(n)+'</span></summary><div class="nav-group-links">'
  for t in g['topics']:nav+='<a href="'+prefix+t['file']+'"'+(' aria-current="page"' if p.name==t['file'] else '')+'>'+escape(t['title'])+'</a>'
  nav+='</div></details>'
 nav+='</nav>';s=re.sub(r'<nav aria-label="Topics">.*?</nav>',lambda _:nav,s,count=1,flags=re.S)
 header='<nav class="header-links" aria-label="Guide navigation"><a href="'+('engineering_notes.html' if p.parent==ROOT.parent else '../engineering_notes.html')+'"'+(' aria-current="page"' if p.parent==ROOT.parent else '')+'>General tech</a><a href="'+prefix+'system-design.html"'+(' aria-current="true"' if area=='system-design' else '')+'>System design</a><a href="'+prefix+'tags.html" data-browse-tags'+(' aria-current="page"' if p.name=='tags.html' else '')+'>Browse by tag</a></nav><!-- header-links -->'
 s=re.sub(r'<nav class="header-links".*?</nav><!-- header-links -->',lambda _:header,s,count=1,flags=re.S)
 if own:
  flat=[t for g in visible for t in g['topics']];idx=next(i for i,t in enumerate(flat) if t['file']==p.name)
  adjacent='<nav class="page-navigation" aria-label="Adjacent topics">'
  if idx:adjacent+='<a href="'+flat[idx-1]['file']+'">Previous: '+escape(flat[idx-1]['title'])+'</a>'
  if idx+1<len(flat):adjacent+='<a href="'+flat[idx+1]['file']+'">Next: '+escape(flat[idx+1]['title'])+'</a>'
  adjacent+='</nav>';s=re.sub(r'<nav class="page-navigation".*?</nav>',lambda _:adjacent,s,count=1,flags=re.S)
 p.write_text(s)
print('Updated navigation for engineering and system-design tracks.')
