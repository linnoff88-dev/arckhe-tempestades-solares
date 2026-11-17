"""Build + check + render + som + QA de um vídeo v3 (refação visual). Mesmo avatar e alinhamento.
Uso: python3 render_v3.py <config.json> [--so-build]"""
import json, os, subprocess, sys
from pathlib import Path

EV = Path('/home/nmaldaner/projetos/explicavideos')
FILA = '/home/nmaldaner/projetos/wifi/scripts/fila-vaga'
TRILHA = '/home/nmaldaner/projetos/inemavox/jobs/audio_library/music/freesound_595385_Star_walk_-_Cinematic_Atmo_Amb_Fantasy_S.mp3'
cfg_path = Path(sys.argv[1]).resolve()
cfg = json.loads(cfg_path.read_text())
out = Path(cfg['output'])
env = dict(os.environ, EXPLICAVIDEOS_CONFIG=str(cfg_path), DISPLAY=':99',
           HYPERFRAMES_BROWSER_PATH='/home/nmaldaner/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux-arm64/chrome-headless-shell')


def run(cmd, timeout=21600):
    print('>>', *map(str, cmd), flush=True)
    subprocess.run(list(map(str, cmd)), cwd=EV, env=env, check=True, timeout=timeout)



CAPA_ATE = {'solar-equipamentos': 'Essa', 'solar-noaa-painel': 'Você', 'solar-historia-protecao': 'Essa'}


def legenda_apos_capa(index, palavra):
    """Capa (quadro 0) já traz a pergunta escrita: legenda só aparece quando a capa sai (2ª frase)."""
    import re as _re
    html = index.read_text()
    if 'legenda-apos-capa' in html:
        return
    caps = json.loads(_re.search(r'window\.CAPS=(.*?);</script>', html, _re.S).group(1))
    t = next(g['s'] for g in caps if g['w'][0]['w'].strip(',.?!').lower() == palavra.lower())
    html = html.replace('window.__timelines["main"]=tl;',
                        f'/*legenda-apos-capa*/tl.set("#caps",{{autoAlpha:0}},0);tl.set("#caps",{{autoAlpha:1}},{t - 0.05:.2f});\n window.__timelines["main"]=tl;', 1)
    index.write_text(html)
    print('legenda depois da capa em', t, flush=True)

blocks = json.loads((out / 'blocos/manifest.json').read_text())
for b in blocks:
    run(['python3', 'engine/v2/build_block.py', b['part']] + (['--strict'] if os.environ.get('STRICT') else []))
    if b['part'] == 1:
        legenda_apos_capa(out / 'final/pt-b01/index.html', CAPA_ATE[cfg['id'].rsplit('-', 1)[0]])
    run(['npx', '--yes', 'hyperframes@0.8.77', 'check', out / 'final' / f"pt-b{b['part']:02d}"], timeout=900)
if '--so-build' in sys.argv:
    sys.exit(0)
run([FILA, 'render', cfg['id'] + '-v3-' + cfg['aspect'].replace(':', ''), '--', 'bash', 'engine/v2/run_lane.sh', *[b['part'] for b in blocks]])
run([FILA, 'render', cfg['id'] + '-v3-montagem', '--', 'python3', 'engine/assemble_languages.py'])
fmt = '916' if cfg['aspect'] == '9:16' else '169'
slug = cfg['id'].rsplit('-', 1)[0]
dest = out.parent / 'entrega-v3'
dest.mkdir(exist_ok=True)
final = dest / f'{slug}-{fmt}.mp4'
run([FILA, 'render', cfg['id'] + '-v3-som', '--', 'python3', 'engine/v2/som_viral.py', out / 'final/pt-b01',
     out / 'final' / f"{cfg['id']}-pt.mp4", final, '--trilha=' + TRILHA, '--sem-efeitos'])
srt = out / 'final' / f"{cfg['id']}-pt.srt"
if srt.exists():
    (dest / (final.stem + '.srt')).write_bytes(srt.read_bytes())
subprocess.run(['python3', 'engine/v2/qa_viral.py', str(final), '--saida=' + str(out / 'verification')], cwd=EV, env=env)
print('PRONTO', final, flush=True)
