import json, subprocess
from pathlib import Path
B=Path(__file__).parent
out=B/'v3'; out.mkdir(exist_ok=True)
items=json.loads((B/'lives10-proposta.json').read_text())
for i,x in enumerate(items):
    dst=out/(Path(x['file']).stem+'-720p.mp4')
    if not dst.exists():
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',x['file']]))
        kb=min(1100,int(43*1048576*8/duration/1000)-96)
        scale='720:1280' if x['format']=='9x16' else '1280:720'
        cmd=['ffmpeg','-y','-v','error','-i',x['file'],'-vf','scale='+scale,'-c:v','libx264','-preset','medium','-b:v',str(kb)+'k','-maxrate',str(int(kb*1.3))+'k','-bufsize',str(kb*2)+'k','-c:a','aac','-b:a','96k','-movflags','+faststart',str(dst)]
        subprocess.run(['/home/nmaldaner/projetos/wifi/scripts/fila-vaga','render','solar-v3-'+str(i),'--']+cmd,check=True,timeout=2400)
    assert dst.stat().st_size<49*1048576
    subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'],check=True,timeout=600)
    caption=x['video']+'\nFormato '+x['format']+' · cópia 720p para Telegram. Original Full HD no repositório.\nConteúdo educativo; chamada hipotética, sem previsão datada.\ninema.club'
    subprocess.run(['node','/home/nmaldaner/projetos/refazvideo/ferramentas/enviar_bot_v3.mjs',str(dst),caption],check=True,timeout=900)
