# Notas de produção

Os cinco MP4 correspondem à entrega original revisada da produção de 16/11/2026. As chamadas são hipóteses educativas, sem previsão datada.

Preferências do Nei registradas depois dessa renderização: evitar movimento repetitivo de aproximação/afastamento da imagem; no CTA, limpar o conteúdo anterior e exibir logo oficial ou inema.club, estendendo a cena se necessário. Essas preferências estão registradas para os próximos trabalhos; não houve nova renderização desses cinco arquivos para aplicá-las.

Os vídeos contêm legendas gravadas na imagem. Os SRT separados estão no Release. O OAuth atual do Lives10 não permite enviar uma trilha opcional de legendas; renovar a autorização do canal para habilitar essa função.

## Refação visual v3 (17/11/2026)

O Nei achou os vídeos fracos. Diagnóstico: nenhum corte seco, o mesmo slide até 40 s na tela (o quadro "Antes de faltar luz" ocupava quase metade do vídeo de impacto), cerca de 12 imagens recicladas nos 8 min do longo, capa que não combinava com o resto, legenda sobre o rodapé dos slides e sobre a capa no quadro 0.

O que mudou, com a mesma fala e o mesmo avatar (sem HeyGen novo):
- 60 ilustrações geradas pelo Codex `image_gen` (assinatura), uma por momento, sem texto; pedidos em `producao/v3/pedido-imagens-*.txt`.
- Troca de conteúdo a cada 2–4 s (36 trocas no vídeo de impacto, 49 no da NOAA, 126 no longo), câmera parada (D22).
- Prints da NOAA ampliados em recortes legíveis. Classes A–X em gráfico de barras. 1989, 2024 e 1859 em tela de capítulo. Carimbos "SEM % DE APAGÃO" e "X ≠ APAGÃO".
- Legenda escondida enquanto a capa está na tela. CTA em tela limpa com o logo INEMA.CLUB.
- O motor no modo estrito pede troca a cada 2 s (padrão de reel). Aqui o limite foi de 3–4 s, por ser explicativo 16:9; o build saiu sem `--strict`, com `hyperframes check` sem erro.
- Limite conhecido: no 9:16, os prints do painel da NOAA ficam pequenos.

Lives10: cada vídeo novo subiu no mesmo horário. O antigo ficou privado e fora da agenda, sem ser apagado (`conteudo/trocas-lives10.json`).
