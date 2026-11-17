"""Libera o pacote completo e avisa o Nei. Somente GitHub e Telegram autorizados.

Não chama a API do YouTube, não agenda e não reenvia avatares.
"""
import hashlib,json,re,subprocess,time,urllib.request
from pathlib import Path

R=Path(__file__).resolve().parent
REPO='inematds/explicavideos';TAG='videos-solares-20261116'
URL=f'https://github.com/{REPO}/releases/tag/{TAG}'
SLUGS=['solar-equipamentos','solar-noaa-painel','solar-historia-protecao']
KINDS=['impacto','noaa','longo']
EXPECTED=[('solar-equipamentos','169'),('solar-equipamentos','916'),('solar-noaa-painel','169'),('solar-noaa-painel','916'),('solar-historia-protecao','169')]

def run(cmd,**kwargs):
 return subprocess.run(list(map(str,cmd)),check=True,text=True,capture_output=True,timeout=kwargs.pop('timeout',1800),**kwargs)
def notify(message):
 p=run(['bash','/home/nmaldaner/projetos/wifi/scripts/avisa-v3.sh',message],timeout=60)
 assert 'HTTP 200' in p.stdout,p.stdout
 m=re.search(r'msg (\d+)',p.stdout);assert m,p.stdout
 return int(m.group(1))
def release_data():
 data=json.loads(run(['gh','api',f'repos/{REPO}/releases']).stdout)
 return next(d for d in data if d['tag_name']==TAG)
def main():
 receipt=R/'ENTREGA.json'
 if receipt.exists():print(receipt.read_text());return
 assert (R/'REVISAO-VISUAL-APROVADA').exists(),'Sem revisão visual'
 # Work is bounded, and a failed render causes an explicit failure notification.
 for _ in range(720):
  files=[]
  for slug,fmt in EXPECTED:
   p=Path('/home/nmaldaner/projetos/output')/(slug+'-20261116')/'entrega'/f'{slug}-{fmt}.mp4'
   files.append(p)
  if all(p.exists() and Path(str(p)+'.qa.json').exists() for p in files):
   for p in files:
    q=json.loads(Path(str(p)+'.qa.json').read_text());assert q['ok'],f'QA reprovado: {p.name}: {q.get("motivo")}'
   if all((R/s/'arquivos-produzidos.json').exists() for s in SLUGS):break
  for k in KINDS:
   s=run(['systemctl','--user','show',f'solar-render-{k}-20261116.service','--property=ActiveState','--value']).stdout.strip()
   assert s!='failed',f'Renderização interrompida: {k}; ver journalctl da unidade'
  time.sleep(20)
 else:raise RuntimeError('Prazo de 4 h esgotado para o pacote completo')
 assets=[];manifest=[]
 for p in files:
  probe=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','json',p]).stdout)
  assert any(s['codec_type']=='audio' for s in probe['streams']),p.name+' sem áudio'
  assert p.stat().st_size>1000000,p.name+' incompleto'
  srt=p.with_suffix('.srt');assert srt.exists(),srt
  assets += [p,srt]
  manifest.append(dict(name=p.name,bytes=p.stat().st_size,duration=float(probe['format']['duration']),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),qa='aprovado',visual_review='quadros conferidos'))
 for n in ['capa-impacto.png','capa-impacto-916.png','capa-noaa-v2.png','capa-noaa-v2-916.png','capa-longo.png']:assets.append(R/'media'/n)
 assets.append(R/'FONTES-E-CREDITOS.txt')
 public_manifest=R/'ARQUIVOS.json';public_manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');assets.append(public_manifest)
 remote=release_data();byname={a['name']:a for a in remote['assets']}
 for p in assets:
  if p.name in byname:
   a=byname[p.name];assert a['size']==p.stat().st_size and a['state']=='uploaded',p.name+' remoto incompleto'
   if a.get('digest'):assert a['digest']=='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest(),p.name+' hash divergente'
  else:run(['gh','release','upload',TAG,p,'--repo',REPO],timeout=2400)
 # Check every uploaded asset's bytes and digest before publishing.
 remote=release_data();byname={a['name']:a for a in remote['assets']}
 for p in assets:
  a=byname[p.name];assert a['state']=='uploaded' and a['size']==p.stat().st_size,p.name
  if a.get('digest'):assert a['digest']=='sha256:'+hashlib.sha256(p.read_bytes()).hexdigest(),p.name
 run(['gh','release','edit',TAG,'--repo',REPO,'--draft=false','--latest=false','--notes-file',R/'release-notes.md'])
 assert not release_data()['draft'],'Release continua em rascunho'
 with urllib.request.urlopen(URL,timeout=45) as response:assert response.status==200
 for p in files:
  req=urllib.request.Request(f'https://github.com/{REPO}/releases/download/{TAG}/{p.name}',method='HEAD')
  with urllib.request.urlopen(req,timeout=45) as response:assert response.status==200
 message=('✅ Terminei os três vídeos independentes sobre tempestades solares, com seu avatar.\n\n'
 '• Explosão solar e equipamentos — 1min42s, horizontal e vertical.\n'
 '• NOAA e seus painéis — 2min07s, horizontal e vertical.\n'
 '• História, fenômenos e proteção — 8min11s, horizontal.\n\n'
 'Link para baixar as 5 versões em MP4, legendas e capas:\n'+URL+'\n\n'
 'Arquivos conferidos e disponíveis. O Lives10 ainda não foi agendado: a regra do seu AGENTS.md exige autorização expressa para a API do YouTube. A proposta de um vídeo diferente por dia está preparada.')
 mid=notify(message)
 receipt.write_text(json.dumps(dict(url=URL,telegram_message=mid,assets=[p.name for p in assets],youtube_scheduled=False,verified_http=True),ensure_ascii=False,indent=2)+'\n')
 (R/'STATUS.txt').write_text('PACOTE COMPLETO: 3 vídeos independentes, 5 versões MP4, QA aprovado, download HTTP 200.\n'+URL+'\nAviso enviado ao bot v3, mensagem '+str(mid)+'.\nLives10 ainda não agendado; exige autorização expressa de API YouTube.\n')
 print(receipt.read_text(),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as exc:
  message='⚠ Produção solar: a entrega não foi concluída. '+type(exc).__name__+': '+str(exc)[:350]+'. Avatares preservados; nenhum reenvio e nenhum agendamento automático no YouTube.'
  (R/'ENTREGA-FALHOU.txt').write_text(message+'\n')
  if not (R/'FALHA-AVISADA').exists():
   mid=notify(message);(R/'FALHA-AVISADA').write_text(str(mid)+'\n')
  raise
