"""Helpers do roteiro visual v3 (refação 17/11/2026). Padrão: explicavideos PADRAO-VIRAL + inema-design D22.
Câmera parada; o movimento vem da troca de imagem. Uma imagem por momento, sem repetir no mesmo vídeo."""
import json, re
from pathlib import Path
from unicodedata import normalize

REF = Path('/home/nmaldaner/projetos/output/solar-refeito-20261117')
SERIE_MEDIA = Path('/home/nmaldaner/projetos/output/solar-noaa-serie/media')
VIDEOS = json.loads(Path('/home/nmaldaner/projetos/tempestades-solares/conteudo/videos.json').read_text())
LOGO = '/home/nmaldaner/projetos/output/solar-refeito-20261117/imagens/recortes/logo-inema-club-169.png'
ILUS = 'ILUSTRAÇÃO · SEM ESCALA'


def img(nome):
    """Imagem gerada (Codex) da biblioteca, ou mídia da série (prints NOAA, diagramas, clipes NASA)."""
    for p in list((REF / 'imagens').glob('*/' + nome + '.png')) + [SERIE_MEDIA / nome]:
        if p.exists():
            return str(p)
    for ext in ('.png', '.jpg', '.mp4'):
        p = SERIE_MEDIA / (nome + ext)
        if p.exists():
            return str(p)
    raise FileNotFoundError(nome)


def foto(nome, at, fonte=None, tag=None, texto=False, av='mini'):
    sh = {'type': 'foto', 'at': at, 'src': img(nome), 'zoom': [1, 1.03], 'focus': [.5, .5], 'av': av}
    if texto:
        sh['texto'] = True
        sh['leitura'] = True
    if fonte:
        sh['fonte'] = fonte
    if tag:
        sh['tag'] = tag
    return sh


def gerada(nome, at, av='mini'):
    return foto(nome, at, fonte='Ilustração gerada para este vídeo', av=av)


def kin(nome, at, palavras, size=110):
    return {'type': 'cinetica', 'at': at, 'src': img(nome), 'size': size, 'av': 'mini',
            'palavras': [dict(t=t, at=a, hl=hl) for t, a, hl in palavras]}


def rosto(nome, at, txt):
    return {'type': 'rosto', 'at': at, 'src': img(nome), 'txt': txt, 'av': 'meia'}


def capitulo(nome, at, text, k, sub=None, sub_at=None):
    sh = {'type': 'capitulo', 'at': at, 'src': img(nome), 'text': text, 'k': k, 'av': 'mini'}
    if sub:
        sh['sub'] = sub
    if sub_at:
        sh['sub_at'] = sub_at
    return sh


def carimbo(at, txt, x=.82, y=.3):
    return {'type': 'carimbo', 'at': at, 'txt': txt, 'x': x, 'y': y, 'keep': True}


def cta(at, url_at=None):
    sh = {'type': 'cta', 'at': at, 'src': LOGO, 'av': 'mini', 'url': '**inema.club**', 'sub': 'Conteúdo aberto e gratuito'}
    if url_at:
        sh['url_at'] = url_at
    return sh


def capa(nome):
    return {'type': 'capa', 'at': '@start', 'src': str(SERIE_MEDIA / nome), 'zoom': [1, 1.01]}


norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())).strip()


def montar(slug, cenas, out_dirs, vertical_dirs=()):
    """cenas: {n: [shots]} → visual-v2/pt-bXX.json em cada saída, conferindo deixas e repetição de imagem."""
    v = next(x for x in VIDEOS if x['slug'] == slug)
    erros, usadas = [], {}
    for n, shots in cenas.items():
        fala = norm(v['cenas'][n - 1]['speech'])
        pos = -1
        for sh in shots:
            def walk(o):
                if isinstance(o, dict):
                    for k, x in o.items():
                        if (k == 'at' or k.endswith('_at')) and isinstance(x, str) and x != '@start':
                            if norm(x.split('#')[0]) not in fala:
                                erros.append((n, k, x))
                        walk(x)
                elif isinstance(o, list):
                    for x in o:
                        walk(x)
            walk(sh)
            if sh['at'] != '@start':
                p = fala.find(norm(sh['at'].split('#')[0]))
                if p < pos:
                    erros.append((n, 'ordem', sh['at']))
                pos = p
            s = sh.get('src')
            if s and sh['type'] in ('foto', 'capitulo') and s != LOGO:
                usadas.setdefault(s, []).append(n)
    rep = {Path(k).name: v for k, v in usadas.items() if len(v) > 1}
    if erros:
        raise SystemExit(f'deixas inválidas: {erros}')
    blocos = {}
    for b in json.loads((Path(out_dirs[0]) / 'blocos/manifest.json').read_text()):
        blocos[b['part']] = b['scenes']
    for d in list(out_dirs) + list(vertical_dirs):
        vertical = d in vertical_dirs
        for part, scenes in blocos.items():
            sc = {}
            for n in scenes:
                shots = json.loads(json.dumps(cenas[n]))
                if vertical:
                    for sh in shots:
                        sh.pop('av', None)   # poses de avatar são do 16:9; no 9:16 vale avatar_916/pip_cena
                        s = sh.get('src', '')
                        alt = Path(s).with_name(Path(s).stem + '-916' + Path(s).suffix) if s else None
                        if alt and alt.exists():
                            sh['src'] = str(alt)
                fundo = next((sh['src'] for sh in shots if sh.get('src') and not sh['src'].endswith('.mp4')), LOGO)
                if any(sh['type'] == 'cta' for sh in shots):
                    fundo = LOGO   # CTA em tela limpa (Nei): nada do conteúdo anterior por trás
                sc[str(n)] = {'takeaway': False, 'header': False, 'fundo': fundo, 'shots': shots}
            p = Path(d) / 'visual-v2' / f'pt-b{part:02d}.json'
            p.write_text(json.dumps({'block': f'pt-b{part:02d}', 'scenes': sc}, ensure_ascii=False, indent=2) + '\n')
    total = sum(len(s) for s in cenas.values())
    print(f'{slug}: {total} shots em {len(cenas)} cenas; imagens repetidas: {rep or "nenhuma"}')
