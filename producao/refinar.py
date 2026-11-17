"""Acrescenta clipes científicos e adapta a leitura para cada formato, antes do render."""
import json,os,subprocess,sys,shutil
from pathlib import Path
R=Path(__file__).resolve().parent;EV=Path('/home/nmaldaner/projetos/explicavideos')
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
slug=sys.argv[1];p=R/slug
videos=json.loads((R/'videos.json').read_text());v=next(x for x in videos if x['slug']==slug)
for config in [p/'v2.json',p/'v2-916.json']:
 if not config.exists():continue
 cfg=json.loads(config.read_text());o=Path(cfg['output']);vertical=cfg['aspect']=='9:16'
 if vertical:
  cfg['pip_cena']=999;cfg['pip_move']=False;dump(config,cfg)
 for f in sorted((o/'visual-v2').glob('pt-b*.json')):
  original=o/'visual-original'/f.name
  original.parent.mkdir(exist_ok=True)
  if not original.exists():shutil.copy2(f,original)
  spec=json.loads(original.read_text())
  for ns,s in spec['scenes'].items():
   n=int(ns);c=v['cenas'][n-1];w=c['speech'].split()
   # Keep each scientific source on screen; no fabricated agency endorsement.
   for sh in s['shots']:
    if sh['type']!='capa':sh['fonte']='NOAA / SWPC · '+('painel usado como exemplo de leitura' if c['arte'] in ['dashboard','goes'] else 'ilustração didática')
    if sh.get('src','').endswith('/capa-noaa.png'):sh['src']=str(R/'media/capa-noaa-v2.png')
    if vertical and sh.get('src'):
     orig=Path(sh['src']);vert=orig.with_name(orig.stem+'-916'+orig.suffix)
     if vert.exists():sh['src']=str(vert)
   selections={
    ('solar-equipamentos',2):('Se ela vier','A mudança do campo','nasa-terra-10s.mp4'),
    ('solar-noaa-painel',2):('Partículas energéticas','Já uma ejeção','nasa-particulas-10s.mp4'),
    ('solar-historia-protecao',4):('Alguns chegam','Essa tempestade','nasa-particulas-10s.mp4'),
    ('solar-historia-protecao',5):('O Sol expulsa','Uma erupção luminosa','nasa-terra-10s.mp4'),
    ('solar-historia-protecao',7):('O campo magnético','Um campo vindo','nasa-terra-10s.mp4'),
   }
   sel=selections.get((slug,n))
   if sel:
    a,b,clip=sel;existing=s['shots'][-1]
    # Add no more than 10 seconds of a clip at its spoken cue; return to diagram.
    video=dict(type='foto',at=a,src=str(R/'media'/clip),zoom=[1,1.02],tag='VISUALIZAÇÃO CIENTÍFICA · SEM ESCALA',fonte='NASA GSFC / Conceptual Image Lab · Bailee DesRocher' if 'terra' in clip else 'NASA GSFC / Conceptual Image Lab · Walt Feimer')
    photo={**existing,'at':b,'pontos':[]}
    # Points before the return cue would violate scene cue order; regenerate later points.
    bi=next(i for i in range(len(w)) if ' '.join(w[i:i+len(b.split())]).strip('.,;:!?').lower()==b.lower())
    photo['pontos']=[dict(at=' '.join(w[i:i+4]).strip('.,;:!?'),focus=[.45,.5],zoom=1.03+(j%2)*.03) for j,i in enumerate(range(bi+7,len(w)-3,7))]
    # Retain only original camera cues preceding the video start.
    ai=next(i for i in range(len(w)) if ' '.join(w[i:i+len(a.split())]).strip('.,;:!?').lower()==a.lower())
    existing['pontos']=[q for q in existing.get('pontos',[]) if c['speech'].find(q['at']) < c['speech'].find(a)]
    s['shots']+=[video,photo]
   details={
    ('solar-noaa-painel',4):[('O gráfico de raios','goes-detalhe.png'),('No coronógrafo','noaa-lasco.jpg'),('O modelo Enlil','noaa-enlil.jpg')],
    ('solar-historia-protecao',2):[('As manchas solares','noaa-sol-real.png')],
    ('solar-historia-protecao',6):[('Buracos coronais','noaa-buracos.jpg')],
    ('solar-historia-protecao',13):[('No gráfico GOES','goes-detalhe.png'),('O coronógrafo','noaa-lasco.jpg')],
   }.get((slug,n),[])
   if details:
    for sh in s['shots']:sh['pontos']=[]
    for at,name in details:
     shot=dict(type='foto',at=at,src=str(R/'media'/name),zoom=[1,1.04],texto=True,leitura=True,tag='EXEMPLO DE LEITURA · IMAGEM DA CAPTURA',fonte='NOAA / SWPC; gráfico GOES: SpaceWeatherLive')
     if at=='No dashboard da NOAA':
      # The actual scales occupy a narrow strip: keep it readable, then explain their meaning.
      shot['zoom']=[1,1.02]
     s['shots'].append(shot)
    def order(sh):
     return -1 if sh['at']=='@start' else c['speech'].find(sh['at'])
    # A detail at the existing shot's opening replaces it.
    bycue={sh['at']:sh for sh in s['shots']}
    s['shots']=sorted(bycue.values(),key=order)
   # Two cue strings can name the same beginning of speech: the replacement wins.
   unique={(-1 if sh['at']=='@start' else c['speech'].find(sh['at'])):sh for sh in s['shots']}
   s['shots']=[unique[k] for k in sorted(unique)]
   # Reframe readable diagrams and charts inside each shot's spoken interval.
   # Detail substitutions must retain camera movement until the next spoken cue.
   for j,sh in enumerate(s['shots']):
    if sh['type']!='foto' or str(sh.get('src','')).endswith('.mp4'):continue
    start_char=c['speech'].find(sh['at'])
    end_char=c['speech'].find(s['shots'][j+1]['at']) if j+1<len(s['shots']) else len(c['speech'])
    assert start_char>=0 and end_char>start_char,(slug,n,sh['at'])
    start_word=len(c['speech'][:start_char].split());end_word=len(c['speech'][:end_char].split())
    sh['pontos']=[dict(at=' '.join(w[i:min(i+3,end_word)]).strip('.,;:!?'),focus=[.44 if z%2==0 else .49,.47 if z%2==0 else .53],zoom=1.03+(z%2)*.03) for z,i in enumerate(range(start_word+5,end_word-1,5))]
   # Make final CTA visible over a relevant illustration, without promising an unbuilt kit.
   if n==len(v['cenas']):s['shots'][-1]['tag']='INEMA.CLUB · APRENDA PARA SE PREPARAR'
  dump(f,spec)
  part=int(f.stem[-2:]);env=dict(os.environ,EXPLICAVIDEOS_CONFIG=str(config))
  subprocess.run(['python3','engine/v2/build_block.py',str(part),'--strict'],cwd=EV,env=env,check=True)
 if vertical:
  for index in (o/'final').glob('pt-b*/index.html'):
   markup=index.read_text()
   if 'solar-caption-safe' not in markup:
    index.write_text(markup.replace('</head>','<style id="solar-caption-safe">.viral.v916 #caps{top:950px!important;height:160px!important}</style></head>',1))
print('REFINO_CONCLUIDO',slug)
