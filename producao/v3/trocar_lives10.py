"""Troca um vídeo agendado no Lives10 pela versão v3: sobe o novo no MESMO horário, confere,
e só então tira o antigo do agendamento (fica privado, sem publishAt — reversível; nada é apagado).
Uso: python3 trocar_lives10.py <índice 0-4> <novo.mp4> <novo.srt>"""
import json, os, re, runpy, subprocess, sys
from datetime import datetime
from pathlib import Path
import requests
from PIL import Image

SERIE = Path('/home/nmaldaner/projetos/output/solar-noaa-serie')
REF = Path('/home/nmaldaner/projetos/output/solar-refeito-20261117')
CLI = '/home/nmaldaner/projetos/yt-pubx/yt-pubx'
EXPECTED = 'UCSWmQN1X3aOMHF_tR9uNuIg'
api = runpy.run_path(CLI, run_name='ytpubx_read')
nome, c = api['canal'](api['load_config'](), 'lives10')
H = lambda: {'Authorization': 'Bearer ' + api['access_token'](nome, c)}


def get(resource, **params):
    r = requests.get('https://www.googleapis.com/youtube/v3/' + resource, params=params, headers=H(), timeout=60)
    r.raise_for_status()
    return r.json()


i, novo, srt = int(sys.argv[1]), sys.argv[2], sys.argv[3]
x = json.loads((SERIE / 'lives10-proposta.json').read_text())[i]
old = json.loads((SERIE / 'lives10-recibos.json').read_text())[i]
assert old['origem'] == x['file'], 'recibo e proposta não batem'
old_id = old['video_id']
ov = get('videos', part='snippet,status', id=old_id)['items'][0]
assert ov['snippet']['channelId'] == EXPECTED
print('ANTIGO', old_id, ov['status'].get('privacyStatus'), ov['status'].get('publishAt'), flush=True)

cover = ['capa-impacto.png', None, 'capa-noaa-v2.png', None, 'capa-longo.png'][i]
args = [CLI, 'publicar', novo, '--canal', 'lives10', '--title', x['video'],
        '--description', Path(x['description']).read_text().split('\n\n', 1)[1],
        '--tags', 'Sol,NOAA,clima espacial,tempestade solar,INEMA', '--legenda', srt, '--avulso-ok', '--repetir',
        '--agendar', x['proposed_publish_local']]
if cover:
    thumb = REF / f'thumb-{i}.jpg'
    Image.open(SERIE / 'media' / cover).convert('RGB').resize((1280, 720)).save(thumb, quality=92)
    args += ['--thumb', str(thumb)]
else:
    args += ['--sem-thumb']
env = dict(os.environ, TZ='America/Sao_Paulo')
dry = subprocess.run(args + ['--dry-run'], capture_output=True, text=True, env=env, timeout=180)
(REF / 'logs' / f'lives10-{i}-dry.log').write_text(dry.stdout + dry.stderr)
assert dry.returncode == 0, dry.stderr[-2000:]
plan = re.search(r'PLANO: (.+)', dry.stdout).group(1).strip()
with (REF / 'logs' / f'lives10-{i}-upload.log').open('w') as log:
    p = subprocess.run(args + ['--plano', plan], stdout=log, stderr=subprocess.STDOUT, env=env, timeout=2400)
assert p.returncode == 0, f'upload {i} falhou; ver logs/lives10-{i}-upload.log antes de repetir'
lines = [json.loads(l) for l in Path(api['HISTORICO']).read_text().splitlines() if l.strip()]
rec = next(t for t in reversed(lines) if t.get('canal') == 'lives10' and t.get('origem') == novo)
nv = get('videos', part='snippet,status', id=rec['video_id'])['items'][0]
assert nv['snippet']['channelId'] == EXPECTED and nv['status']['privacyStatus'] == 'private'
assert datetime.fromisoformat(nv['status']['publishAt'].replace('Z', '+00:00')) == datetime.fromisoformat(ov['status']['publishAt'].replace('Z', '+00:00')), 'horário diferente'
print('NOVO', rec['video_id'], nv['status']['publishAt'], flush=True)

# Tira o antigo do agendamento: privado, sem publishAt (reversível pelo Studio).
body = {'id': old_id, 'status': {'privacyStatus': 'private', 'selfDeclaredMadeForKids': False,
                                  'embeddable': ov['status'].get('embeddable', True),
                                  'license': ov['status'].get('license', 'youtube'),
                                  'publicStatsViewable': ov['status'].get('publicStatsViewable', True)}}
r = requests.put('https://www.googleapis.com/youtube/v3/videos', params={'part': 'status'}, json=body, headers=H(), timeout=60)
r.raise_for_status()
ov2 = get('videos', part='status', id=old_id)['items'][0]['status']
assert ov2['privacyStatus'] == 'private' and not ov2.get('publishAt'), ov2
print('ANTIGO DESAGENDADO', old_id, flush=True)
trocas = REF / 'trocas-lives10.json'
d = json.loads(trocas.read_text()) if trocas.exists() else []
d.append({'indice': i, 'titulo': x['video'], 'antigo': old_id, 'antigo_status': ov2, 'novo': rec['video_id'],
          'url': rec.get('url'), 'publishAt': nv['status']['publishAt'], 'arquivo': novo,
          'legenda_ok': rec.get('legenda_ok'), 'thumb_ok': rec.get('thumb_ok')})
trocas.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
