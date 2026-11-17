"""Conclui arquivos locais após o HeyGen. Publicação é uma etapa separada."""
import json,os,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;EV=Path('/home/nmaldaner/projetos/explicavideos');FILA='/home/nmaldaner/projetos/wifi/scripts/fila-vaga'
slug=sys.argv[1];kind=sys.argv[2];p=R/slug;unit=f'solar-montar-{kind}-20261116.service'
def run(cmd,env=None,cwd=EV,timeout=21600):
 print('Executando:',*map(str,cmd),flush=True)
 return subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,check=True,timeout=timeout)
for _ in range(1500):
 st=subprocess.check_output(['systemctl','--user','show',unit,'--property=ActiveState','--value'],text=True).strip()
 if st in ['failed','inactive']:
  code=subprocess.check_output(['systemctl','--user','show',unit,'--property=ExecMainStatus','--value'],text=True).strip()
  assert code=='0',f'Montagem falhou: {unit}, status {code}'
  assert (p/'VISUAL-CONSTRUIDO').exists(),'Montagem saiu sem construir o visual'
  break
 time.sleep(20)
else:raise RuntimeError('Prazo da montagem esgotado')
run(['python3',R/'refinar.py',slug])
receipts=[]
for config in [p/'v2.json',p/'v2-916.json']:
 if not config.exists():continue
 cfg=json.loads(config.read_text());out=Path(cfg['output']);env=dict(os.environ,EXPLICAVIDEOS_CONFIG=str(config),HYPERFRAMES_BROWSER_PATH='/home/nmaldaner/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux-arm64/chrome-headless-shell')
 blocks=json.loads((out/'blocos/manifest.json').read_text())
 for b in blocks:
  key=f"pt-b{b['part']:02d}";project=out/'final'/key
  # Actual HyperFrames checks and snapshots precede delivery rendering.
  run(['npx','--yes','hyperframes@0.8.77','check',project],env=env,timeout=900)
  al=json.loads((project/'alignment.json').read_text());starts=al['starts'];dur=al['duration']
  points=[0]+[round(min(dur-.2,t+2),2) for t in starts[:-1]]
  run(['npx','--yes','hyperframes@0.8.77','snapshot',project,'--at',','.join(map(str,points)),'--describe','false','--output',out/'verification'/f'quadros-{key}'],env=env,timeout=1200)
 # The editable compositions are kept; preview can be served from these folders.
 run([FILA,'render',slug+'-'+cfg['aspect'],'--','bash','engine/v2/run_lane.sh',*[b['part'] for b in blocks]],env=env)
 run([FILA,'render',slug+'-montagem','--','python3','engine/assemble_languages.py'],env=env)
 dest=out.parent/'entrega';dest.mkdir(exist_ok=True)
 fmt='916' if cfg['aspect']=='9:16' else '169';final=dest/f'{slug}-{fmt}.mp4'
 track='/home/nmaldaner/projetos/inemavox/jobs/audio_library/music/freesound_595385_Star_walk_-_Cinematic_Atmo_Amb_Fantasy_S.mp3'
 run([FILA,'render',slug+'-som','--','python3','engine/v2/som_viral.py',out/'final/pt-b01',out/'final'/f"{cfg['id']}-pt.mp4",final,'--trilha='+track,'--sem-efeitos'],env=env)
 # Technical QA is evidence; it does not replace looking at the produced frames.
 run([FILA,'render',slug+'-qa','--','python3','engine/v2/qa_viral.py',final,'--saida='+str(out/'verification')],env=env,timeout=1800)
 run(['ffmpeg','-v','error','-i',final,'-f','null','-'],timeout=3600)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','json',str(final)]))
 assert any(s.get('codec_type')=='audio' for s in probe['streams'])
 expected=(1080,1920) if fmt=='916' else (1920,1080)
 assert any((s.get('width'),s.get('height'))==expected for s in probe['streams'])
 srt=out/'final'/f"{cfg['id']}-pt.srt"
 if srt.exists(): (dest/(final.stem+'.srt')).write_bytes(srt.read_bytes())
 receipts.append(dict(file=str(final),probe=probe,technical_qa='passed',visual_review='pending',published=False))
(p/'arquivos-produzidos.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
(p/'STATUS.txt').write_text('Arquivos produzidos e QA técnico aprovado. Revisão visual final e publicação/agendamento ainda pendentes.\n')
print('ARQUIVOS_PRODUZIDOS',slug,flush=True)
