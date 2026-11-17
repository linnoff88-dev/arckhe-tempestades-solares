import json, os, re, runpy, subprocess
from pathlib import Path
import requests
from PIL import Image
B=Path(__file__).parent
CLI='/home/nmaldaner/projetos/yt-pubx/yt-pubx'
api=runpy.run_path(CLI,run_name='ytpubx_read')
nome,c=api['canal'](api['load_config'](),'lives10')
expected='UCSWmQN1X3aOMHF_tR9uNuIg'
def get(resource,**params):
    r=requests.get('https://www.googleapis.com/youtube/v3/'+resource,params=params,headers={'Authorization':'Bearer '+api['access_token'](nome,c)},timeout=60)
    r.raise_for_status(); return r.json()
assert get('channels',part='snippet',mine='true')['items'][0]['id']==expected
items=json.loads((B/'lives10-proposta.json').read_text())
receipts=[]
for i,x in enumerate(items):
    cover=['capa-impacto.png',None,'capa-noaa-v2.png',None,'capa-longo.png'][i]
    args=[CLI,'publicar',x['file'],'--canal','lives10','--title',x['video'],'--description',Path(x['description']).read_text().split('\n\n',1)[1],'--tags','Sol,NOAA,clima espacial,tempestade solar,INEMA','--legenda',x['captions'],'--avulso-ok','--agendar',x['proposed_publish_local']]
    if cover:
        thumb=B/(f'lives10-thumb-{i}.jpg')
        Image.open(B/'media'/cover).convert('RGB').resize((1280,720)).save(thumb,quality=92)
        args+=['--thumb',str(thumb)]
    else: args+=['--sem-thumb']
    env=dict(os.environ,TZ='America/Sao_Paulo')
    dry=subprocess.run(args+['--dry-run'],capture_output=True,text=True,env=env,timeout=180)
    (B/f'lives10-{i}-dry.log').write_text(dry.stdout+dry.stderr)
    assert dry.returncode==0,dry.stderr
    plan=re.search(r'PLANO: (.+)',dry.stdout).group(1).strip()
    with (B/f'lives10-{i}-upload.log').open('w') as log:
        p=subprocess.run(args+['--plano',plan],stdout=log,stderr=subprocess.STDOUT,env=env,timeout=2400)
    assert p.returncode==0, f'upload {i} erro; reconciliar log antes de repetir'
    lines=Path(api['HISTORICO']).read_text().splitlines()
    matches=[json.loads(l) for l in lines if l.strip()]
    receipt=next(t for t in reversed(matches) if t.get('canal')=='lives10' and t.get('origem')==x['file'])
    v=get('videos',part='snippet,status',id=receipt['video_id'])['items'][0]
    assert v['snippet']['channelId']==expected
    assert v['status']['privacyStatus']=='private'
    from datetime import datetime
    assert datetime.fromisoformat(v['status']['publishAt'].replace('Z','+00:00'))==datetime.fromisoformat(receipt['privacy']['publishAt'])
    assert receipt['legenda_ok'] is True
    if cover: assert receipt['thumb_ok'] is True
    receipt['verified_status']=v['status']; receipt['verified_channel_id']=expected
    receipts.append(receipt)
    (B/'lives10-recibos.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
    print('AGENDADO',receipt['url'],receipt['privacy']['publishAt'],flush=True)
