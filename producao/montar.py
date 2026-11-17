"""Produção local retomável. Não publica, agenda nem chama modelos por API."""
import json,os,re,shutil,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;EV=Path('/home/nmaldaner/projetos/explicavideos')
FILA='/home/nmaldaner/projetos/wifi/scripts/fila-vaga'
def run(args,env=None,timeout=21600):
 print('Executando:',*[str(x) for x in args],flush=True)
 subprocess.run([str(x) for x in args],cwd=EV,env=env,check=True,timeout=timeout)
def cfg_env(cfg):return dict(os.environ,EXPLICAVIDEOS_CONFIG=str(cfg),DISPLAY=':99')
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copy2(src,dst)
def asset(c):
 return R/'media'/(dict(goes='erupcoes-pt').get(c['arte'],c['arte'])+'.png')
def cue(words,i,n=4):
 return ' '.join(words[i:i+n]).strip(' ,.;:!?')
def visual(v,b,o,vertical):
 scenes={}
 for n in b['scenes']:
  c=v['cenas'][n-1];w=c['speech'].split();src=asset(c)
  assert src.exists(),src
  shots=[];first=0
  if n==1:
   shots.append(dict(type='capa',at='@start',src=str(src),zoom=[1,1.015],texto=True))
   # Preserve the complete question/hook; change at its following sentence.
   first=next((i+1 for i,x in enumerate(w) if x.endswith(('?','.','!'))),min(15,len(w)-1))
  if first<len(w):
   main=src
   if n==1:main=R/'media'/('dashboard.png' if v['slug']=='solar-noaa-painel' else 'mecanismo.png')
   # One explanatory image stays long enough to read. Speech cues move its camera.
   pts=[]
   for j,i in enumerate(range(first+7,len(w)-2,7)):
    pts.append(dict(at=cue(w,i),focus=[.42 if j%2==0 else .47,.45 if j%2==0 else .53],zoom=1.03+(j%3)*.025))
   sh=dict(type='foto',at=cue(w,first),src=str(main),zoom=[1,1.05],focus=[.46,.5],pontos=pts,texto=True,leitura=True)
   # Website footage is a demonstration, not a bulletin for a date.
   if c['arte'] in ['dashboard','goes'] or (n==1 and v['slug']=='solar-noaa-painel'):
    sh['tag']='EXEMPLO DE LEITURA · CONSULTE O PAINEL ATUAL'
   shots.append(sh)
  scenes[str(n)]=dict(shots=shots,fundo=str(src),header=False,takeaway=False)
 (o/'visual-v2'/f"pt-b{b['part']:02d}.json").write_text(json.dumps(dict(block=f"pt-b{b['part']:02d}",scenes=scenes),ensure_ascii=False,indent=2)+'\n')

def main(slug):
 p=R/slug;v=next(x for x in json.loads((R/'videos.json').read_text()) if x['slug']==slug)
 cfg=p/'v1.json';vc=json.loads(cfg.read_text());o=Path(vc['output']);manifest=o/'blocos/manifest.json'
 # Wait for only the existing studio submissions; never send/re-send here.
 for _ in range(360):
  blocks=json.loads(manifest.read_text())
  if all(b.get('id') for b in blocks):break
  if any(b.get('status')=='needs_review' for b in blocks):raise RuntimeError('Submissão precisa de conferência; não reenviar')
  time.sleep(10)
 else:raise RuntimeError('IDs do estúdio não chegaram em 1h')
 run(['/home/nmaldaner/projetos/refazvideo/ferramentas/baixa_blocos.sh',o.parent],timeout=23000)
 for b in blocks:
  key=f"pt-b{b['part']:02d}";trans=o/'verification'/f'transcript-{key}.json';asr=o/'inemavox'/key
  if not trans.exists():
   run([FILA,'gpu',slug+'-transcricao','--','python3','/home/nmaldaner/projetos/inemavox/transcrever_v1.py','--in',o/'assets'/f'nei-{key}.mp4','--outdir',asr,'--whisper-model','large-v3','--src','pt','--words'],timeout=14400)
   words=json.loads((asr/'words.json').read_text());assert len(words)>100
   d=dict(words=words,text=' '.join(w['word'] for w in words),transcriber='inemavox-whisper-local')
   trans.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  mp3=o/'assets'/f'nei-{key}.mp3'
  if not mp3.exists():run(['ffmpeg','-v','error','-y','-i',o/'assets'/f'nei-{key}.mp4','-vn','-ar','16000','-ac','1','-b:a','64k',mp3])
  # Alignment is measured against the actual avatar. No v1 rendering or fabricated assembled receipt.
  run(['python3','engine/build_final_block.py','pt',b['part']],env=cfg_env(cfg))
 for config in [p/'v2.json',p/'v2-916.json']:
  if not config.exists():continue
  c=json.loads(config.read_text());out=Path(c['output']);vertical=c['aspect']=='9:16'
  for d in ['assets','blocos','docs','verification','final','align','visual-v2','logs']:(out/d).mkdir(parents=True,exist_ok=True)
  copy(manifest,out/'blocos/manifest.json');copy(o/'docs/lesson-pt.json',out/'docs/lesson-pt.json');copy(o/'verification/blocos-downloads.json',out/'verification/blocos-downloads.json')
  for b in blocks:
   key=f"pt-b{b['part']:02d}"
   copy(o/'verification'/f'transcript-{key}.json',out/'verification'/f'transcript-{key}.json')
   copy(o/'final'/key/'alignment.json',out/'align'/f'{key}.json')
   for ext in ['mp4','mp3']:
    link=out/'assets'/f'nei-{key}.{ext}'
    if not link.exists():link.symlink_to((o/'assets'/f'nei-{key}.{ext}').resolve())
   visual(v,b,out,vertical)
   run(['python3','engine/v2/build_block.py',b['part'],'--strict'],env=cfg_env(config))
  (p/'VISUAL-CONSTRUIDO').write_text('Roteiro visual construído com transcrição real; falta revisão por snapshots.\n')
 print('BUILD_CONCLUIDO',slug,flush=True)

if __name__=='__main__':main(sys.argv[1])
