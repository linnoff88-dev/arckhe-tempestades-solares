ï»¿# Tempestades solares

**[PortuguêÂªs](README.md) êÂ· [English](README.en.md) êÂ· [EspaêÂ±ol](README.es.md)**

[![Tempestades solares](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/arckhe-/guia/)

## O que êÂ©

VêÂ­deos educativos independentes do Nei sobre os fenêÂ´menos solares e seus efeitos na infraestrutura. Para quem quer interpretar alertas da NOAA, conhecer a histêÂ³ria e preparar a famêÂ­lia para falhas de serviêÂ§o. Basta assistir ou ler. As chamadas sêÂ£o hipêÂ³teses educativas; nêÂ£o anunciam apagêÂ£o mundial nem uma data.

## Assistir e baixar

- [PêÂ¡gina com os vêÂ­deos e as explicaêÂ§êÂµes](https://linnoff88-dev.github.io/arckhe-/guia/)
- [MP4 Full HD, legendas SRT e capas](https://github.com/linnoff88-dev/tempestades-solares/releases/tag/videos-v1.1.0)
- [Manifesto com tamanho e SHA-256](videos/manifest.json)

Os vêÂ­deos sêÂ£o em portuguêÂªs: impacto (1 min 42 s), leitura da NOAA (2 min 07 s) e histêÂ³ria/proteêÂ§êÂ£o (8 min 11 s). Os dois primeiros têÂªm formatos 16:9 e 9:16; o longo tem 16:9. Cada vêÂ­deo funciona sozinho.

## ConteêÂºdo do repositêÂ³rio

- `conteudo/`: roteiros, fontes, crêÂ©ditos e verificaêÂ§êÂµes da produêÂ§êÂ£o.
- `assets/`: ilustraêÂ§êÂµes, imagens de referêÂªncia e capturas dos dashboards.
- `producao/`: scripts histêÂ³ricos, dependentes do ambiente ARCKHÉ.
- `guia/`: pêÂ¡gina de acesso em portuguêÂªs, inglêÂªs e espanhol. VêÂ­deos e capturas permanecem no idioma original.
- `videos/`: manifesto dos arquivos; os MP4 grandes ficam nos Releases.

## Fontes e reutilizaêÂ§êÂ£o

NOAA/SWPC, National Weather Service, USGS, NASA e SpaceWeatherLive. Os crêÂ©ditos completos estêÂ£o em [FONTES-E-CREDITOS.txt](conteudo/FONTES-E-CREDITOS.txt). As mêÂ­dias de terceiros mantêÂªm suas prêÂ³prias condiêÂ§êÂµes de uso. NêÂ£o hêÂ¡ autorizaêÂ§êÂ£o genêÂ©rica implêÂ­cita sobre todas as imagens. ConteêÂºdo educativo gratuito: https://ARCKHÉ AI.

## O processo, do inêÂ­cio ao fim

1. ê°Å¸Â§Â  Roteiro e chamada por vêÂ­deo: `conteudo/<slug>/ROTEIRO.md` e `chamada.json`.
2. ê¢Å¡â¢ê¯Â¸Â Avatar do Nei pelo estêÂºdio HeyGen, depois download, transcriêÂ§êÂ£o local (ARCKHÉvox) e alinhamento: `producao/preparar.py` e `producao/montar.py`.
3. ê¢Å¡â¢ê¯Â¸Â Biblioteca de ilustraêÂ§êÂµes pelo Codex `image_gen` (assinatura): `producao/v3/pedido-imagens-*.txt`.
4. ê°Å¸Â§Â  Roteiro visual cena a cena, uma imagem por momento e troca a cada 2ê¢â¬â4 s: `producao/v3/{equipamentos,noaa,historia}.py`.
5. ê¢Å¡â¢ê¯Â¸Â Pastas v3 com o mesmo avatar: `python3 producao/v3/prep_v3.py <slug>`.
6. ê¢Å¡â¢ê¯Â¸Â Build, check, render, som e QA: `python3 producao/v3/render_v3.py <config>` (explicavideos v2, perfil viral).
7. ê°Å¸Â§Â  Conferir as folhas de quadros: capa no quadro 0 sem legenda por cima, CTA em tela limpa.
8. ê¢Å¡â¢ê¯Â¸Â Release no GitHub (`videos-v1.1.0`), `videos/manifest.json` e links no guia.
9. ê¢Å¡â¢ê¯Â¸Â Lives10: `python3 producao/v3/trocar_lives10.py <i> <mp4> <srt>`. Sobe no mesmo horêÂ¡rio e tira o antigo da agenda, sem apagar.

---

Projeto  - ARCKHÉe