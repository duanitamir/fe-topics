"""Build offline, accessible SVG architecture sketches and embed them in case studies."""
from pathlib import Path
from html import escape as e
import re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'diagrams';OUT.mkdir(exist_ok=True)
COLORS={'ui':('#edf3ff','#94afd8'),'core':('#f2edfa','#b7a3d0'),'service':('#edf6f1','#94bba4'),'data':('#fff6e6','#c8ae78'),'neutral':('#f3f5f8','#a7b3c5')}
def node(x,y,w,title,lines=(),kind='neutral',h=88):
 fill,stroke=COLORS[kind]
 return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}"/><text x="{x+w/2}" y="{y+29}" text-anchor="middle" font-size="18" font-weight="650">{e(title)}</text>'+''.join(f'<text x="{x+w/2}" y="{y+53+i*20}" text-anchor="middle" font-size="14" fill="#465773">{e(line)}</text>' for i,line in enumerate(lines))+'</g>'
def edge(points,label='',at=None,dashed=False,both=False):
 p=' '.join(f'{x},{y}' for x,y in points)
 line=f'<polyline points="{p}" fill="none" stroke="'+('#477760' if dashed else '#647792')+'" stroke-width="1.7" '+('stroke-dasharray="6 4" ' if dashed else '')+'marker-end="url(#ARROW)" '+('marker-start="url(#START)" ' if both else '')+'/>'
 if label:
  x,y=at or points[len(points)//2];width=len(label)*7.5+16
  line+=f'<g><rect x="{x-width/2}" y="{y-16}" width="{width}" height="24" rx="4" fill="#fff"/><text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="#36516d">{e(label)}</text></g>'
 return line

def svg(name,title,desc,width,height,nodes,edges,extra=''):
 marker=name+'-arrow';start=name+'-start'
 body=''.join(edges).replace('#ARROW','#'+marker).replace('#START','#'+start)+''.join(nodes)+extra
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="{name}-title {name}-desc" font-family="system-ui, sans-serif" fill="#17233b"><title id="{name}-title">{e(title)}</title><desc id="{name}-desc">{e(desc)}</desc><defs><marker id="{marker}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M1 1L7 4L1 7" fill="none" stroke="#647792" stroke-width="1.4"/></marker><marker id="{start}" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M7 1L1 4L7 7" fill="none" stroke="#647792" stroke-width="1.4"/></marker></defs><rect width="{width}" height="{height}" fill="#fff"/>'+body+'</svg>'
DIAGRAMS={}
DIAGRAMS['chat-system']=svg('chat-system','Chat system: durable write and live fanout','HTTPS and WSS enter through a load balancer. The message service writes messages and outbox atomically. A relay publishes to a broker; fanout looks up device routes and sends events through gateways. History reads recover missed events.',1100,850,[
 node(360,25,350,'Browser clients',['Sender, recipient and other devices'],'ui'),
 node(360,180,350,'Load balancer',['HTTPS / WSS; readiness and draining'],'neutral'),
 node(30,350,280,'HTTP application',['History and membership endpoints'],'service'),
 node(390,350,300,'WebSocket gateways',['Socket ownership; bounded buffers'],'service'),
 node(780,350,280,'Connection directory',['User/device → gateway + epoch'],'data'),
 node(30,540,280,'Message service',['Authorize, deduplicate, sequence'],'service'),
 node(30,730,280,'Message database',['Messages + transactional outbox'],'data'),
 node(390,730,300,'Outbox relay',['Retry committed publication'],'service'),
 node(780,540,280,'Durable broker',['Committed message events'],'data'),
 node(780,730,280,'Fanout workers',['Deliver; handle duplicates'],'service')],[
 edge([(535,113),(535,180)],'HTTPS / WSS',(610,154),both=True),
 edge([(410,268),(410,305),(170,305),(170,350)],'HTTP requests',(250,300),both=True),
 edge([(540,268),(540,350)],'WS commands / events',(640,315),both=True),
 edge([(170,438),(170,540)],'application calls',(170,495),both=True),
 edge([(540,438),(540,584),(310,584)],'send / receipt commands',(445,570)),
 edge([(170,628),(170,730)],'transaction / query',(175,690),both=True),
 edge([(310,774),(390,774)],'outbox',(350,756)),
 edge([(690,774),(735,774),(735,584),(780,584)],'publish',(735,675)),
 edge([(920,628),(920,730)],'consume',(925,685)),
 edge([(1060,774),(1080,774),(1080,394),(1060,394)],'route lookup',(1020,485),dashed=True),
 edge([(780,774),(720,774),(720,470),(690,470),(690,394)],'live events to owning gateway',(565,463),dashed=True)
])
DIAGRAMS['chat-components']=svg('chat-components','Chat frontend: route, components and shared data','Solid arrows show page composition and props. Dashed arrows show runtime commands and data subscriptions. URL owns conversation selection; Composer owns draft; the message cache owns remote snapshots; the realtime adapter reconciles socket events.',1000,880,[
 node(320,25,360,'ChatRoute / page',['URL conversationId; layout and loaders'],'ui'),
 node(40,195,280,'ConversationList',['Summaries; navigation links'],'ui'),
 node(540,195,380,'ConversationPanel',['Selected conversation and scoped actions'],'ui'),
 node(380,365,240,'MessageList',['Pages, scroll and virtualization'],'ui'),
 node(690,365,240,'Composer',['Local draft; pending feedback'],'ui'),
 node(380,535,240,'MessageRow',['Message text and receipt state'],'ui'),
 node(40,730,390,'Server-state message cache',['Canonical messages, receipts and cursors'],'data'),
 node(590,730,340,'Realtime / API adapter',['WS lifecycle; HTTP history + sends'],'service')],[
 edge([(370,113),(370,150),(180,150),(180,195)],'props',(210,147)),
 edge([(630,113),(630,150),(730,150),(730,195)],'conversationId',(775,147)),
 edge([(600,283),(600,325),(500,325),(500,365)],'items / callbacks',(465,320)),
 edge([(800,283),(800,365)],'submit callback',(875,325)),
 edge([(500,453),(500,535)],'message props',(590,500)),
 edge([(810,453),(960,453),(960,774),(930,774)],'send intent',(912,635),dashed=True),
 edge([(590,774),(430,774)],'merge / invalidate',(510,754),dashed=True),
 edge([(230,730),(230,410),(380,410)],'subscribe / render',(240,510),dashed=True),
 edge([(120,730),(120,283)],'summary subscription',(130,615),dashed=True)
])
DIAGRAMS['ac-components']=svg('ac-components','Autocomplete: host page and component composition','The host form imports the React entry point. The root owns one controller instance and distributes bindings. Input emits query/key events, Option emits selection events, and the adapter reads snapshots. DOM focus stays on the input.',1000,850,[
 node(300,25,400,'Host page / Form',['Domain value; validation; API/cache adapter'],'ui'),
 node(300,195,400,'Autocomplete.Root',['One scoped owner; controlled prop contract'],'ui'),
 node(35,385,260,'Autocomplete.Input',['Query, key and composition events'],'ui'),
 node(365,385,270,'Autocomplete.Results',['Listbox; loading/empty/error states'],'ui'),
 node(705,385,260,'Autocomplete.Status',['Polite feedback and safe retry UI'],'ui'),
 node(365,565,270,'Autocomplete.Option × N',['Stable key / ID; pointer selection'],'ui'),
 node(265,745,470,'React adapter + controller instance',['Subscriptions, state snapshots and semantic callbacks'],'core')],[
 edge([(500,113),(500,195)],'props ↓ / onChange ↑',(630,155),both=True),
 edge([(360,283),(360,335),(165,335),(165,385)],'input bindings',(190,330)),
 edge([(500,283),(500,385)],'items / activeKey',(590,340)),
 edge([(640,283),(640,335),(835,335),(835,385)],'request status',(830,330)),
 edge([(500,473),(500,565)],'item props',(580,520)),
 edge([(165,473),(165,790),(265,790)],'input / key events',(165,660),dashed=True),
 edge([(500,653),(500,745)],'SELECT(key)',(590,705),dashed=True),
 edge([(735,790),(985,790),(985,240),(700,240)],'snapshot subscription',(865,690),dashed=True)
])
DIAGRAMS['ac-system']=svg('ac-system','Autocomplete: core, framework adapter and data boundary','Host props enter the React adapter, which dispatches events and reads immutable snapshots from a TypeScript controller. A pure reducer updates state. An async coordinator owns request generation and cancellation; an injected source accesses a local index or remote API/cache.',1000,860,[
 node(290,25,420,'Host application',['Item model, labels, keys, auth/cache scope'],'ui'),
 node(290,195,420,'React adapter + optional UI',['Bindings, stable IDs, lifecycle and subscriptions'],'ui'),
 node(35,395,400,'Framework-independent controller',['Immutable snapshot; dispatch and subscribe'],'core'),
 node(570,395,390,'Async coordinator',['Debounce, AbortSignal, generation guards'],'core'),
 node(35,595,400,'Pure reducer / selectors',['Valid transitions; derived active/selected state'],'core'),
 node(570,595,390,'Injected DataSource<T>',['Host adapter; validation; cache/cancellation policy'],'service'),
 node(570,755,390,'Local index OR remote API/cache',['No hard-coded endpoint or global personalized cache'],'data')],[
 edge([(500,113),(500,195)],'config / controlled changes',(650,155),both=True),
 edge([(370,283),(370,335),(235,335),(235,395)],'dispatch / snapshots',(240,330),both=True),
 edge([(435,439),(570,439)],'jobs / results',(500,420),both=True),
 edge([(235,483),(235,595)],'state + event → next state',(245,550),both=True),
 edge([(765,483),(765,595)],'query + signal / items or error',(775,550),both=True),
 edge([(765,683),(765,755)],'local call OR HTTPS',(765,725),both=True)
])

def sequence(name,title,desc,actors,events,note):
 width=1100;xs=[100+i*225 for i in range(len(actors))];height=180+len(events)*85
 nodes=[node(x-92,20,184,label,[],kind='neutral',h=58) for x,label in zip(xs,actors)]
 extra=''.join(f'<line x1="{x}" y1="78" x2="{x}" y2="{height-35}" stroke="#bcc8d8" stroke-dasharray="5 5"/>' for x in xs)
 edges=[]
 for i,(a,b,label,dashed) in enumerate(events):
  y=125+i*85;edges.append(edge([(xs[a],y),(xs[b],y)],str(i+1)+'. '+label,((xs[a]+xs[b])/2,y-10),dashed=dashed))
 extra+=f'<text x="30" y="{height-8}" font-size="13" fill="#465773">{e(note)}</text>'
 return svg(name,title,desc,width,height,nodes,edges,extra=extra)
DIAGRAMS['chat-sequence']=sequence('chat-sequence','Send sequence: durable acceptance before delivery','Time moves downward. The service commits a message and outbox before acknowledging the sender; asynchronous relay/fanout reaches the recipient. A lost acknowledgement is resolved by retrying the same clientMessageId.',['Sender UI','Message service','Database/outbox','Relay / fanout','Recipient UI'],[
(0,1,'send stable clientMessageId',False),(1,2,'authorize + dedupe + commit',False),(2,1,'durable result + sequence',True),(1,0,'accepted (canonical ID)',True),(2,3,'poll committed outbox → publish',False),(3,4,'message event via gateway',False),(4,1,'device delivery acknowledgement',True),(0,1,'retry same key if uncertain',False),(1,0,'original stored result',True)],'Gateway/broker hops are expanded in the system diagram. Dashed arrows are replies/acknowledgements.')
DIAGRAMS['ac-sequence']=sequence('ac-sequence','Async query sequence: newer input owns the result','Time moves downward. Input starts a debounced query through the controller and coordinator. New input aborts old work; a stale completion is ignored even if cancellation is not honored. Only the current result is rendered.',['Input / UI','Controller','Coordinator','Data source','Host page'],[
(0,1,'INPUT: a',False),(1,2,'debounce then request A',False),(2,3,'query a + AbortSignal',False),(0,1,'INPUT: al',False),(1,2,'invalidate A; request B',False),(2,3,'abort A; query al',False),(3,2,'B results (current)',True),(2,1,'apply generation B',True),(1,0,'snapshot → render options',True),(3,2,'late A result: ignored',True),(0,1,'SELECT stable item key',False),(1,4,'onValueChange(item, reason)',False)],'Controlled selection commits only when the host echoes the new value; onChange is a request, not a forced mutation.')

def figure(name,title,note,old_attrs=''):
 svg_source=DIAGRAMS[name];(OUT/(name+'.svg')).write_text(svg_source+'\n')
 return '<figure'+old_attrs+' class="flow-diagram communication-diagram" aria-labelledby="'+name+'-caption"><figcaption id="'+name+'-caption">'+title+'</figcaption><p class="diagram-controls"><a href="diagrams/'+name+'.svg" target="_blank" rel="noopener">Open full-size diagram</a><span>Scroll horizontally on smaller screens.</span></p><div class="diagram-viewport" role="region" aria-label="'+e(title,quote=True)+'" tabindex="0">'+svg_source+'</div><p class="flow-note">'+note+'</p></figure>'

def replace_figure(page,old_caption,name,title,note):
 s=page.read_text();m=re.search(r'<figure\b(?P<attrs>[^>]*)aria-labelledby="'+old_caption+r'".*?</figure>',s,re.S)
 if not m:
  # Regeneration updates only the generated SVG inside the new figure.
  m=re.search(r'<figure\b(?P<attrs>[^>]*)aria-labelledby="'+name+r'-caption".*?</figure>',s,re.S)
 assert m,(page,old_caption)
 old_ids=re.findall(r'\bid="([^"]+)"',m[0]);attrs=''
 # Preserve the original figure ID; preserve its authored caption as a hidden alias.
 figid=re.search(r'<figure[^>]*\bid="([^"]+)"',m[0])
 if figid:attrs=' id="'+figid[1]+'"'
 alias='<span class="anchor-alias" id="'+old_caption+'"></span>'
 new=figure(name,title,note,attrs)
 # Keep old caption anchors at the same semantic figure location.
 new=new.replace('<figcaption',alias+'<figcaption',1)
 s=s[:m.start()]+new+s[m.end():];page.write_text(s)

def upsert_card(page,id,title,body,before):
 s=page.read_text();content='<section class="reading-card" aria-labelledby="'+id+'"><h2 id="'+id+'">'+title+'</h2>'+body+'</section>'
 m=re.search(r'<section class="reading-card" aria-labelledby="'+id+r'">.*?</section>',s,re.S)
 if m:s=s[:m.start()]+content+s[m.end():]
 else:
  pos=s.index('<section class="reading-card" aria-labelledby="'+before+'">');s=s[:pos]+content+s[pos:]
  entry='<li><a href="#'+id+'">'+title+'</a></li>';pos=s.index('<a href="#'+before+'">');pos=s.rfind('<li',0,pos);s=s[:pos]+entry+s[pos:]
 page.write_text(s)
def append_figure(page,section,name,title,note):
 s=page.read_text();m=re.search(r'<figure[^>]*aria-labelledby="'+name+r'-caption".*?</figure>',s,re.S);new=figure(name,title,note)
 if m:s=s[:m.start()]+new+s[m.end():]
 else:
  pos=s.index('<section class="reading-card" aria-labelledby="'+section+'">');pos=s.index('</section>',pos);s=s[:pos]+new+s[pos:]
 page.write_text(s)
chat=ROOT/'system-design-chat.html';ac=ROOT/'system-design-autocomplete.html'
replace_figure(chat,'chat-architecture-caption','chat-system','System sketch · chat services and communication','Solid arrows show commands, calls and durable publication; dashed paths show transient routing/delivery. The connection directory is consulted for device routes. Accepted is returned only after the database commit policy is met; reconnect history uses the HTTP application/database path.')
replace_figure(ac,'ac-architecture-caption','ac-system','Architecture sketch · autocomplete core and data boundary','Arrows name the exchanged contract; paired arrowheads show a request/result or event/snapshot relationship, not a module dependency cycle. The React adapter depends on core interfaces; the core has no React, DOM or host-API dependency.')
upsert_card(chat,'chat-component-map','Frontend sketch · pages, components and data flow','<p id="chat-component-map-definition">Draw the frontend separately from the backend architecture: show what renders what, who owns state, and how interaction reaches the network. Solid arrows below show composition/props; dashed arrows show runtime commands and subscriptions.</p>'+figure('chat-components','Page and component sketch · chat client','The selected conversation comes from the URL. ConversationPanel scopes the interaction; Composer owns the draft. Server-owned messages live in one cache; the network adapter reconciles events into it. Dashed subscriptions are data flow, not child-parent ownership.')+'<p><strong>Sketch it in this order:</strong> Route/layout → visible components → state owner → API/realtime adapter → event/cache updates. Explain one send and one history fetch. Then use the system sketch to expand the server side.</p>','chat-sketches')
upsert_card(ac,'ac-component-map','Component sketch · host page, slots and event paths','<p id="ac-component-map-definition">Draw the consumer page and imported component first, then expand its slots and scoped controller. This is component composition, not a requirement to deploy a service for each box.</p>'+figure('ac-components','Page and component sketch · imported autocomplete','Solid arrows show composition/bindings; dashed arrows show events and snapshot subscription. The root/adapter refers to one controller instance, not a separate controller in every slot. Input keeps DOM focus; Option sends a semantic selection event.')+'<p><strong>Sketch it in this order:</strong> Host form → imported root → input/results/status → option instances → single state owner → injected data source. Keep selected value, query text and active option distinct. Expand the controller/data-source box in the next architecture sketch.</p>','ac-blueprint')
append_figure(chat,'chat-send','chat-sequence','Sequence sketch · one message from send to delivery','Time moves downward. Replies/acknowledgements are dashed. Relay polling is asynchronous; publication may happen before or after the sender observes accepted. The invariant is that both accepted and publication follow commit. The retry at the end illustrates a lost acknowledgement, not an instruction to retry every successful send.')
append_figure(ac,'ac-async','ac-sequence','Sequence sketch · typing, cancellation and selection','Time moves downward. Query B owns the results even if A ignores cancellation. An old completion does not mutate the visible snapshot. A controlled host may accept or reject the proposed value; identity and callback reasons are part of the public API.')
print('Built six offline SVG diagrams and integrated structure, architecture and sequence views.')
