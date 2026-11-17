from lib import *

R = str(REF / 'imagens/recortes') + '/'
NASA_P = 'NASA GSFC / Conceptual Image Lab · Walt Feimer'
EX = 'EXEMPLO DE LEITURA · CONSULTE O PAINEL ATUAL'
def rec(nome, at, fonte='NOAA / SWPC · captura de 16/11/2026', tag=EX):
    return {'type': 'foto', 'at': at, 'src': R + nome + '.png', 'zoom': [1, 1.02], 'focus': [.5, .5], 'av': 'mini',
            'texto': True, 'leitura': True, 'fonte': fonte, 'tag': tag}

C = {
 1: [capa('capa-noaa-v2.png'),
     rosto('aviao-polar', 'Você sabe quando', 'PERIGO PARA QUEM?'),
     kin('casa-sem-luz', 'para a sua casa', [('SUA CASA?', 'para a sua casa', False), ('O AVIÃO?', 'para o avião', False), ('SÓ O RÁDIO?', 'só para o rádio', True)], 110),
     kin('sala-previsao', 'Um alerta sem', [('LETRA', 'sem a letra', True), ('NÍVEL', 'o nível', True), ('VALIDADE', 'a validade', True)], 120),
     rec('painel-rsg', 'Vou mostrar como')],
 2: [capitulo('sol-erupcao', 'Primeiro, separe', 'TRÊS FENÔMENOS', 'PASSO 1 DE 3', 'luz · partículas · nuvem de plasma', 'A erupção libera'),
     gerada('clarao-raiox', 'radiação eletromagnética'),
     {'type': 'bignum', 'at': 'cerca de oito minutos', 'src': img('clarao-raiox'), 'ate': 8, 'unid': ' min', 'k': 'RADIAÇÃO · VELOCIDADE DA LUZ', 'l': 'do Sol até a Terra', 'av': 'mini'},
     gerada('radio-amador', 'pode prejudicar rádio'),
     gerada('particulas-espaco', 'Partículas energéticas'),
     gerada('satelite-orbita', 'ameaçam satélites'),
     gerada('estacao-espacial', 'e astronautas'),
     gerada('aviao-polar', 'a aviação em regiões'),
     gerada('cme-espaco', 'Já uma ejeção'),
     foto('nasa-terra-10s.mp4', 'leva horas a dias', fonte='NASA GSFC / Conceptual Image Lab · Bailee DesRocher', tag='VISUALIZAÇÃO CIENTÍFICA · SEM ESCALA')],
 3: [capitulo('sala-previsao', 'No dashboard', 'R · S · G', 'PASSO 2 DE 3', 'as três letras do painel'),
     rec('painel-rsg', 'procure três letras'),
     kin('radio-amador', 'Erre é interrupção', [('R = RÁDIO', 'interrupção de rádio', True)], 130),
     kin('particulas-espaco', 'Esse é tempestade', [('S = RADIAÇÃO', 'radiação solar', True)], 130),
     kin('terra-magnetosfera', 'Gê é tempestade', [('G = GEOMAGNÉTICA', 'tempestade geomagnética', True)], 120),
     kin('manchas-solares', 'Cada uma vai', [('NÍVEL 1 A 5', 'de um a cinco', True)], 140),
     kin('linhas-transmissao', 'O nível de rádio', [('R ALTO', 'nível de rádio', False), ('≠ REDE EM RISCO', 'rede elétrica', True)], 110),
     rec('painel-graficos', 'Confira também'),
     kin('ceu-noturno-calmo', 'já foi observado', [('OBSERVADO', 'já foi observado', False), ('OU PREVISÃO?', 'uma previsão', True)], 120)],
 4: [rec('goes-zoom', 'O gráfico de raios', fonte='SpaceWeatherLive · dados GOES / NOAA', tag='EXEMPLO DE LEITURA'),
     gerada('antenas-gps', 'satélites GOES'),
     {'type': 'ranking', 'at': 'As classes', 'src': img('clarao-raiox'), 'av': 'mini', 'titulo': 'Raios X: cada classe = 10× a anterior', 'log': True,
      'max': 10000, 'itens': [
        {'n': 'A', 'v': 1, 'txt': '1×', 'at': 'As classes A'}, {'n': 'B', 'v': 10, 'txt': '10×', 'at': 'B, C'},
        {'n': 'C', 'v': 100, 'txt': '100×', 'at': 'C, M'}, {'n': 'M', 'v': 1000, 'txt': '1.000×', 'at': 'M e X'},
        {'n': 'X', 'v': 10000, 'txt': '10.000×', 'hl': True, 'at': 'sobem de dez'}]},
     gerada('cidade-apagao', 'Classe X não'),
     carimbo('apagão garantido', 'X ≠ APAGÃO', x=.5, y=.45),
     foto('noaa-lasco.jpg', 'No coronógrafo', fonte='NOAA / SWPC · coronógrafo LASCO', tag=EX),
     foto('noaa-enlil.jpg', 'O modelo Enlil', fonte='NOAA / SWPC · modelo WSA-Enlil', tag=EX),
     kin('vento-solar', 'São instrumentos diferentes', [('CADA INSTRUMENTO', 'instrumentos diferentes', False), ('UMA PERGUNTA', 'perguntas diferentes', True)], 110)],
 5: [capitulo('sala-controle-rede', 'Abra o painel', 'COMO CONSULTAR', 'PASSO 3 DE 3', 'escala · horário · detalhes', 'Veja a escala'),
     rec('painel-rsg', 'Veja a escala'),
     kin('ceu-noturno-calmo', 'o horário em tempo', [('HORÁRIO UTC', 'tempo universal', True), ('BRASÍLIA = UTC − 3', 'os detalhes', False)], 100),
     kin('sala-previsao', 'Watch indica', [('WATCH', 'Watch indica', True), ('pode acontecer', 'janela futura', False)], 120),
     kin('tecnico-subestacao', 'warning indica', [('WARNING', 'warning indica', True), ('esperado em breve', 'esperada em breve', False)], 120),
     kin('aurora-cidade', 'alert registra', [('ALERT', 'alert registra', True), ('já observado', 'limiar observado', False)], 120),
     rec('painel-texto', 'Leia a mensagem'),
     foto('erupcoes-pt.png', 'O SpaceWeatherLive', fonte='SpaceWeatherLive · em português', tag='EXEMPLO DE LEITURA', texto=True),
     foto('noaa-flare.jpg', 'o boletim da NOAA', fonte='NOAA / SWPC', tag=EX),
     carimbo('Um print antigo', 'PRINT ANTIGO ≠ PREVISÃO', x=.5, y=.5)],
 6: [kin('torre-celular', 'Se o aviso', [('SUA REGIÃO?', 'a sua região', False), ('SIGA OS RESPONSÁVEIS', 'orientações dos responsáveis', True)], 100),
     gerada('familia-plano', 'Para a família'),
     gerada('powerbank-celular', 'baterias carregadas'),
     gerada('trilhos-sinal', 'para satélites'),
     rosto('clarao-raiox', 'Você já tinha', 'CLASSE X = APAGÃO?'),
     kin('celular-notebook', 'Aprenda a conferir', [('CONFIRA', 'conferir', True), ('ANTES DE COMPARTILHAR', 'antes de compartilhar', False)], 110),
     cta('Tem conteúdo gratuito', 'inema ponto club')],
}
O = '/home/nmaldaner/projetos/output/solar-noaa-painel-20261116/'
montar('solar-noaa-painel', C, [O + 'v3'], [O + 'v3-916'])
