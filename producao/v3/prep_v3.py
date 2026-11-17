"""Cria as pastas v3 (refação visual) a partir das v2: mesmo avatar, transcrição e alinhamento; visual novo.
Uso: python3 prep_v3.py <slug>"""
import json, shutil, sys
from pathlib import Path

SERIE = Path('/home/nmaldaner/projetos/output/solar-noaa-serie')
REF = Path('/home/nmaldaner/projetos/output/solar-refeito-20261117')
slug = sys.argv[1]
for nome in ['v2.json', 'v2-916.json']:
    src_cfg = SERIE / slug / nome
    if not src_cfg.exists():
        continue
    cfg = json.loads(src_cfg.read_text())
    old = Path(cfg['output'])
    new = old.parent / old.name.replace('v2', 'v3')
    for d in ['assets', 'blocos', 'docs', 'align', 'visual-v2', 'logs', 'final']:
        (new / d).mkdir(parents=True, exist_ok=True)
    (new / 'verification').mkdir(exist_ok=True)
    for d in ['blocos', 'docs', 'align']:
        for f in (old / d).iterdir():
            if f.is_file() and not (new / d / f.name).exists():
                shutil.copy2(f, new / d / f.name)
    for f in (old / 'verification').glob('*.json'):
        if not (new / 'verification' / f.name).exists():
            shutil.copy2(f, new / 'verification' / f.name)
    for f in (old / 'assets').iterdir():
        link = new / 'assets' / f.name
        if not link.exists():
            link.symlink_to(f.resolve())
    cfg['output'] = str(new)
    if cfg.get('aspect') == '9:16':
        # capa sem avatar -> meio tamanho na cena 1 -> PiP com a cena no quadro inteiro (style.md, D8)
        cfg['pip_cena'] = 2
        cfg['pip_move'] = False
    out_cfg = REF / 'configs' / f"{slug}-{nome.replace('v2', 'v3')}"
    out_cfg.parent.mkdir(exist_ok=True)
    out_cfg.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    print('ok', out_cfg, '->', new)
