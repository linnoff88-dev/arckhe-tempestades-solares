# Tempestades solares

**[PortuguÃªs](README.md) Â· [English](README.en.md) Â· [EspaÃ±ol](README.es.md)**

[![Tempestades solares](guia/assets/banner.jpg)](https://inematds.github.io/tempestades-solares/guia/)

## O que Ã©

VÃ­deos educativos independentes do Nei sobre os fenÃ´menos solares e seus efeitos na infraestrutura. Para quem quer interpretar alertas da NOAA, conhecer a histÃ³ria e preparar a famÃ­lia para falhas de serviÃ§o. Basta assistir ou ler. As chamadas sÃ£o hipÃ³teses educativas; nÃ£o anunciam apagÃ£o mundial nem uma data.

## Assistir e baixar

- [PÃ¡gina com os vÃ­deos e as explicaÃ§Ãµes](https://inematds.github.io/tempestades-solares/guia/)
- [MP4 Full HD, legendas SRT e capas](https://github.com/inematds/tempestades-solares/releases/tag/videos-v1.1.0)
- [Manifesto com tamanho e SHA-256](videos/manifest.json)

Os vÃ­deos sÃ£o em portuguÃªs: impacto (1 min 42 s), leitura da NOAA (2 min 07 s) e histÃ³ria/proteÃ§Ã£o (8 min 11 s). Os dois primeiros tÃªm formatos 16:9 e 9:16; o longo tem 16:9. Cada vÃ­deo funciona sozinho.

## ConteÃºdo do repositÃ³rio

- `conteudo/`: roteiros, fontes, crÃ©ditos e verificaÃ§Ãµes da produÃ§Ã£o.
- `assets/`: ilustraÃ§Ãµes, imagens de referÃªncia e capturas dos dashboards.
- `producao/`: scripts histÃ³ricos, dependentes do ambiente INEMA.
- `guia/`: pÃ¡gina de acesso em portuguÃªs, inglÃªs e espanhol. VÃ­deos e capturas permanecem no idioma original.
- `videos/`: manifesto dos arquivos; os MP4 grandes ficam nos Releases.

## Fontes e reutilizaÃ§Ã£o

NOAA/SWPC, National Weather Service, USGS, NASA e SpaceWeatherLive. Os crÃ©ditos completos estÃ£o em [FONTES-E-CREDITOS.txt](conteudo/FONTES-E-CREDITOS.txt). As mÃ­dias de terceiros mantÃªm suas prÃ³prias condiÃ§Ãµes de uso. NÃ£o hÃ¡ autorizaÃ§Ã£o genÃ©rica implÃ­cita sobre todas as imagens. ConteÃºdo educativo gratuito: https://inema.club.

## O processo, do inÃ­cio ao fim

1. ðŸ§  Roteiro e chamada por vÃ­deo: `conteudo/<slug>/ROTEIRO.md` e `chamada.json`.
2. âš™ï¸ Avatar do Nei pelo estÃºdio HeyGen, depois download, transcriÃ§Ã£o local (inemavox) e alinhamento: `producao/preparar.py` e `producao/montar.py`.
3. âš™ï¸ Biblioteca de ilustraÃ§Ãµes pelo Codex `image_gen` (assinatura): `producao/v3/pedido-imagens-*.txt`.
4. ðŸ§  Roteiro visual cena a cena, uma imagem por momento e troca a cada 2â€“4 s: `producao/v3/{equipamentos,noaa,historia}.py`.
5. âš™ï¸ Pastas v3 com o mesmo avatar: `python3 producao/v3/prep_v3.py <slug>`.
6. âš™ï¸ Build, check, render, som e QA: `python3 producao/v3/render_v3.py <config>` (explicavideos v2, perfil viral).
7. ðŸ§  Conferir as folhas de quadros: capa no quadro 0 sem legenda por cima, CTA em tela limpa.
8. âš™ï¸ Release no GitHub (`videos-v1.1.0`), `videos/manifest.json` e links no guia.
9. âš™ï¸ Lives10: `python3 producao/v3/trocar_lives10.py <i> <mp4> <srt>`. Sobe no mesmo horÃ¡rio e tira o antigo da agenda, sem apagar.

---

Projeto adaptado da comunidade INEMA TDS - Marca Arckhe