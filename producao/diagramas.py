from pathlib import Path
from html import escape
R=Path(__file__).resolve().parent/'media';R.mkdir(exist_ok=True)
def text(x,y,t,size=44,color='#e9f2ff'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-family="DejaVu Sans,sans-serif" font-weight="bold">{escape(t)}</text>'
def line(x1,y1,x2,y2,color='#47d8fa',width=8):
 return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{width}" fill="none" marker-end="url(#arrow)"/>'
def rect(x,y,w,h,color='#142b45',rx=24):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{color}" stroke="#42617c" stroke-width="2"/>'
def sun(x,y,r=110):
 import math
 rays=''.join(f'<path d="M{x+math.cos(i)*r*1.15},{y+math.sin(i)*r*1.15} L{x+math.cos(i)*r*1.4},{y+math.sin(i)*r*1.4}" stroke="#fa9d39" stroke-width="7"/>' for i in [j*math.pi/12 for j in range(24)])
 return rays+f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#sun)"/>'+f'<path d="M{x-45},{y-40} C{x-125},{y-200} {x+155},{y-230} {x+75},{y-45}" fill="none" stroke="#ffca79" stroke-width="13"/>'
def earth(x,y,r=100):
 return f'<circle cx="{x}" cy="{y}" r="{r+10}" fill="#1db3f9" opacity=".22"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#earth)"/>'+f'<path d="M{x-45},{y-r+25} l50,15 30,35 -20,45 -35,15 10,65 -35,-25 -15,-60 -25,-20 Z" fill="#53c8a4"/>'
def card(x,y,title,sub,w=540,h=170):
 return rect(x,y,w,h)+text(x+28,y+62,title,43)+text(x+28,y+115,sub,29,'#99c8dd')
def write(name,title,sub,body,source='NOAA / SWPC · esquema didático, sem escala'):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs>
 <radialGradient id="sun"><stop stop-color="#fff0a0"/><stop offset=".5" stop-color="#ffad35"/><stop offset="1" stop-color="#d85212"/></radialGradient>
 <radialGradient id="earth" cx=".25" cy=".25"><stop stop-color="#39c1f8"/><stop offset=".7" stop-color="#1472b0"/><stop offset="1" stop-color="#062c53"/></radialGradient>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#15324e"/><stop offset="1" stop-color="#061321"/></linearGradient>
 <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#47d8fa"/></marker></defs>
 <rect width="1920" height="1080" fill="url(#bg)"/><g opacity=".09" stroke="#96d4ed">'''+''.join(f'<path d="M0,{i} H1920 M{i},0 V1080"/>' for i in range(0,1920,80))+f'''</g>
 {text(85,105,title,64)}{text(88,163,sub,29,'#99c8dd')}{body}
 {text(85,1025,source,22,'#83a0b9')}{text(1540,1025,'INEMA.CLUB',24,'#ffce71')}</svg>'''
 (R/(name+'.svg')).write_text(svg)

write('mecanismo','DO SOL ATÉ A TOMADA','Plasma e campo magnético podem perturbar o ambiente da Terra.',
 sun(260,420)+earth(1000,420)+line(430,420,820,420)+text(480,365,'NUVEM DE PLASMA',36,'#ffce71')+text(485,480,'horas a dias',40)+
 card(95,680,'1 · SOL','Ejeção de massa coronal')+card(735,680,'2 · TERRA','Perturbação geomagnética')+line(650,760,720,760)+text(160,940,'A direção e o campo magnético fazem diferença.',40,'#ffce71'))
body=''
for y,letter,title,subtitle in [(245,'R','RADIAÇÃO ELETROMAGNÉTICA','Rádio · chega em cerca de 8 minutos'),(470,'S','PARTÍCULAS ENERGÉTICAS','Satélites e espaço · dezenas de minutos ou menos'),(695,'G','TEMPESTADE GEOMAGNÉTICA','Resposta da Terra · pode afetar a rede elétrica')]:
 body+=rect(90,y,1200,190)+f'<circle cx="190" cy="{y+95}" r="64" fill="#124e71"/>'+text(157,y+117,letter,70,'#ffce71')+text(290,y+76,title,39)+text(290,y+133,subtitle,31,'#9dd4ed')
write('fenomenos','TRÊS RISCOS DIFERENTES','R, S e G classificam efeitos; não são nomes de uma mesma explosão.',body)
body=sun(330,470,160)
for j in range(5):
 body+=f'<ellipse cx="330" cy="470" rx="{200+j*23}" ry="{120+j*25}" stroke="#ffc16c" fill="none" stroke-width="4" transform="rotate({j*28} 330 470)" opacity=".65"/>'
body+=card(760,275,'PLASMA','Partículas com carga elétrica')+card(760,510,'CAMPOS MAGNÉTICOS','Movimento, tensão e reorganização')+text(110,865,'Manchas e buracos coronais são fenômenos distintos.',35,'#ffce71')+text(110,930,'Ciclo solar: aproximadamente 11 anos.',40)
write('sol','UM SOL EM MOVIMENTO','Ilustração conceitual; linhas representam campos magnéticos.',body)
body=earth(620,500,150)
for k in [0,1,2]:
 body+=f'<path d="M1480,{250+k*70} C150,{80+k*60} 150,{950-k*60} 1480,{760-k*60}" stroke="#52cbf2" fill="none" stroke-width="5" opacity=".7"/>'
for y in [400,500,600]:body+=line(95,y,350,y)
body+=text(92,320,'VENTO SOLAR',38,'#ffce71')+text(825,505,'MAGNETOSFERA',43)+card(95,800,'IONOSFERA','Altera propagação de rádio',550,150)+card(740,800,'ATMOSFERA SUPERIOR','Aquecimento e arrasto',550,150)
write('terra','A TERRA RESPONDE','A interação depende da intensidade, direção e duração do campo.',body)
body=earth(1020,450,110)
for j in range(12):
 x=120+(j%4)*170;y=280+(j//4)*130
 body+=f'<circle cx="{x}" cy="{y}" r="15" fill="#ffce71"/>'+line(x+24,y,x+100,y)
body+=card(95,730,'PRÓTONS ENERGÉTICOS','Podem afetar circuitos no espaço',600,170)+card(760,730,'PROTEÇÃO TERRESTRE','Atmosfera reduz exposição no solo',600,170)+text(95,650,'Satélites · astronautas · aviação polar',42,'#ffce71')
write('particulas','A RADIAÇÃO SOLAR','A exposição no espaço não é a mesma que na superfície.',body)
body=''
for x in [220,590]:
 body+=f'<path d="M{x-80},650 L{x},280 L{x+80},650 M{x-62},575 H{x+62} M{x-48},500 H{x+48} M{x-28},400 H{x+28}" fill="none" stroke="#9bb9c9" stroke-width="12"/>'
for y in [340,400,460]:body+=f'<path d="M120,{y} Q400,{y+85} 700,{y}" fill="none" stroke="#ffce71" stroke-width="7"/>'
body+=line(730,495,900,495)+rect(945,350,260,290,'#1b5471')+text(960,445,'TRAFO',49)+text(950,515,'CALOR',41,'#ffb064')+text(100,720,'Correntes induzidas em grandes circuitos',42)+card(95,800,'PROTEÇÕES E OPERAÇÃO','Danos e apagões dependem da rede',1200,150)
write('rede','ONDE O RISCO SE CONCENTRA','Uma falha na infraestrutura pode tirar o serviço da sua casa.',body)
body=''
for i,(title,sub) in enumerate([('LUZ','Lanterna e pilhas'),('ENERGIA','Bateria externa carregada'),('ÁGUA E COMIDA','Reserva de itens essenciais'),('COMUNICAÇÃO','Contatos e plano da família')]):
 x=95+(i%2)*630;y=255+(i//2)*260
 body+=card(x,y,title,sub,570,200)
body+=text(95,920,'Dependência médica: planeje reserva e local de apoio.',35,'#ffce71')
write('kit','ANTES DE FALTAR LUZ','Preparação que também ajuda em apagões comuns.',body,'NWS / NOAA · weather.gov/safety/space-before')
body=''
for y,year,title,sub in [(250,'1859','CARRINGTON','Perturbações em telégrafos'),(475,'1989','QUEBEC','Apagão em uma rede moderna'),(700,'2024','TEMPESTADE G5','Não houve apagão mundial')]:
 body+=rect(95,y,1200,175)+text(125,y+105,year,76,'#ffce71')+text(410,y+70,title,46)+text(410,y+125,sub,33)
write('historia','O QUE JÁ ACONTECEU','História real; intensidade não determina sozinha a consequência.',body,'NOAA / SWPC e USGS · registros históricos')
body=text(105,340,'G5',160,'#ffce71')+text(460,330,'CATEGORIA EXTREMA',48)+text(460,405,'~4 ocorrências por ciclo de 11 anos',38)+rect(95,530,1200,195)+text(125,610,'G5 ≠ CARRINGTON',65)+text(125,680,'G5 ≠ APAGÃO MUNDIAL',59,'#ffce71')+text(105,850,'Frequência do fenômeno não é chance de catástrofe.',37)+text(105,915,'A consequência depende também da infraestrutura.',36,'#a8cde0')
write('probabilidade','CHANCE DE QUÊ, EXATAMENTE?','O resultado precisa ser definido antes de falar em probabilidade.',body,'NOAA Space Weather Scales · média histórica, não previsão')
print('9 diagramas vetoriais preparados')
