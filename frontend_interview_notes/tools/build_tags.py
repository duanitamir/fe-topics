"""Build curated passage tags and the offline cross-topic tag browser.
Edit tags.json, then run this script before build_search_index.py.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,re
from tag_icons import icon, ICONS
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'tags.json').read_text());labels=config['tags'];assigned=config['passages']
assert set(labels) <= set(ICONS), 'Every tag needs an icon'
class Text(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_data(self,d):self.parts.append(d)
def plain(s):
 p=Text();p.feed(s);return re.sub(r'\s+',' ',''.join(p.parts)).strip()
def chips(tags):
 return '<nav class="passage-tags" aria-label="Related tags">'+''.join('<a class="tag" href="tags.html?tag='+t+'">'+icon(t)+'<span class="tag-label">'+escape(labels[t])+'</span></a>' for t in tags)+'</nav>'
groups=json.loads((ROOT/'topics.json').read_text());topics=[t for g in groups for t in g['topics']];records=[];seen=set()
for topic in topics:
 p=ROOT/topic['file'];s=p.read_text();s=re.sub(r'<nav class="(?:card-tags|passage-tags)".*?</nav>','',s,flags=re.S)
 def update(m):
  anchor=m['anchor']
  if anchor not in assigned:return m[0]
  tags=assigned[anchor]['tags'];seen.add(anchor)
  assert 1<=len(tags)<=3 and len(tags)==len(set(tags))
  for tag in tags:assert tag in labels,tag
  # The match belongs to a specific explanation, not its enclosing reading card.
  card_start=s.rfind('<section class="reading-card"',0,m.start())
  prefix=s[card_start:m.start()]
  headings=re.findall(r'<h[234]\b[^>]*>(.*?)</h[234]>',prefix,re.S)
  card_title=plain(headings[0]) if headings else ''
  local_title=plain(m['body']) if m['tag']=='h3' else plain(headings[-1]) if headings else card_title
  title=card_title+' › '+local_title if card_title and local_title!=card_title else local_title
  if m['tag']=='p':text=plain(m['body'])
  else:
   following=s[m.end():s.find('</section>',m.end())]
   following=re.split(r'<h[23]\b',following,maxsplit=1)[0]
   paragraph=re.search(r'<p\b[^>]*>(.*?)</p>',following,re.S)
   text=plain(paragraph[1]) if paragraph else plain(following)
  excerpt=text[:240].rsplit(' ',1)[0]+'…' if len(text)>240 else text
  records.append({'title':title,'topic':topic['title'],'page':p.name,'anchor':anchor,'tags':tags,'excerpt':excerpt})
  return m[0]+chips(tags)
 s=re.sub(r'<(?P<tag>h3|p)\b[^>]*\bid="(?P<anchor>[^\"]+)"[^>]*>(?P<body>.*?)</(?P=tag)>',update,s,flags=re.S)
 p.write_text(s)
assert seen==set(assigned),(seen^set(assigned))
# Reuse the search page's familiar topic navigation and accessible responsive shell.
shell=(ROOT/'search.html').read_text();shell=shell.replace('<title>Search ·','<title>Browse by tag ·').replace('class="search-page"','class="tag-page"')
counts={t:sum(t in x['tags'] for x in records) for t in labels}
filters='<nav class="tag-filters" aria-label="Filter cards by tag"><a class="tag" href="tags.html" data-tag-filter="">'+icon('all')+'<span class="tag-label">All explanations</span> <span>'+str(len(records))+'</span></a>'
for tag,label in sorted(labels.items(),key=lambda x:x[1]):filters+='<a class="tag" href="tags.html?tag='+tag+'" data-tag-filter="'+tag+'">'+icon(tag)+'<span class="tag-label">'+escape(label)+'</span> <span>'+str(counts[tag])+'</span></a>'
filters+='</nav>'
results='<ol class="tag-results" data-tag-results aria-label="Tagged explanations">'
for x in records:
 results+='<li data-passage-tags="'+' '.join(x['tags'])+'" data-topic="'+escape(x['topic'],quote=True)+'"><p class="search-result-meta">'+escape(x['topic'])+'</p><h2><a href="'+x['page']+'#'+x['anchor']+'">'+escape(x['title'])+'</a></h2><p>'+escape(x['excerpt'])+'</p>'+chips(x['tags'])+'</li>'
results+='</ol>'
body='<main id="page-start"><p class="breadcrumb"><a href="../frontend_interview_notes.html">All topics</a></p><header><h1>Browse by tag</h1><p class="lead">Follow a concept across topics. Choose a tag to find related explanations and subsections.</p></header>'+filters+'<p class="search-status" data-tag-status role="status" aria-live="polite">'+str(len(records))+' explanations across '+str(len(topics))+' topics.</p>'+results+'<noscript><p>All explanations are listed below the tags. Enable JavaScript to filter by tag.</p></noscript></main>'
shell=re.sub(r'<main\b[^>]*>.*?</main>',lambda m:body,shell,flags=re.S).replace('<script src="search-index.js" defer></script>','<script src="tags.js" defer></script>')
shell=shell.replace('data-header-topic>Search your notes</a>', 'data-header-topic>Browse by tag</a>')
(ROOT/'tags.html').write_text(shell)
# Keep tag browsing reachable from every topic, search, index, and the tag browser itself.
for p in [*ROOT.glob('*.html'),ROOT.parent/'frontend_interview_notes.html']:
 s=p.read_text();s=re.sub(r'<a[^>]*data-browse-tags[^>]*>Browse by tag</a>','',s)
 prefix='frontend_interview_notes/' if p.parent==ROOT.parent else ''
 link='<a href="'+prefix+'tags.html" data-browse-tags'+(' aria-current="page"' if p.name=='tags.html' else '')+'>Browse by tag</a>'
 s=s.replace('</nav><!-- header-links -->',link+'</nav><!-- header-links -->',1)
 p.write_text(s)
print(f'Tagged {len(records)} explanations across {len(topics)} topics using {len(labels)} curated tags.')
