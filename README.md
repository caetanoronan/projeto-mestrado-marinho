# 🌊 Projeto de Mestrado - Biodiversidade e Invasões Marinhas

**Ilhas Costeiras de Santa Catarina**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Online-success)](https://caetanoronan.github.io/projeto-mestrado-marinho/)

## 📋 Sobre o Projeto

Projeto de mestrado proposto para o **PPGOceano/UFSC - 2026** focando em:
- 🔬 Perda de biodiversidade marinha bentônica
- 🦠 Impacto de espécies invasoras (coral-sol)
- 🏝️ Três áreas de estudo em Santa Catarina

## 🗺️ Áreas de Estudo

1. **REBIO Marinha do Arvoredo** - 17.131,72 ha
2. **Ilha do Campeche** - 76,19 ha
3. **Ilha Xavier** - 16,98 ha

## 🎯 Objetivos

Avaliar padrões de biodiversidade e invasões ao longo de gradientes de:
- Tamanho de ilha
- Isolamento geográfico
- Pressão antrópica

## 🔗 Acesse a Apresentação

👉 **[Apresentação Completa do Projeto](Apresentacao_Projeto_Mestrado_Publica.html)**

👉 **[Apresentação Pública de Macrófitas](https://caetanoronan.github.io/projeto-mestrado-marinho/Apresentacao_Macrofitas_Publica.html)**

👉 **[QR Code da apresentação de Macrófitas (PNG)](https://caetanoronan.github.io/projeto-mestrado-marinho/qr_apresentacao_macrofitas.png)**

👉 **[QR Code da apresentação de Macrófitas (SVG)](https://caetanoronan.github.io/projeto-mestrado-marinho/qr_apresentacao_macrofitas.svg)**

## 📊 Conteúdo


### 🪸 Manguezais de Santa Catarina (em preparação)

Este repositório inclui um pipeline para mapear os manguezais de Santa Catarina a partir de fontes oficiais:

- Fonte principal: Global Mangrove Watch (GMW) v3.0 (2020, UNEP-WCMC)
- Alternativas: Atlas dos Manguezais do Brasil (ICMBio/MMA) e MapBiomas Manguezais
- Recorte geográfico: limite estadual (IBGE, SIRGAS 2000)
- Projeções: entrada WGS84 (EPSG:4326); mapas em Web Mercator (EPSG:3857); métricas em SIRGAS 2000 / UTM 22S (EPSG:31982)

Saídas esperadas (serão geradas automaticamente pelo script):

- `Mapas_Gerados/manguezais_sc_gmw.gpkg` — GeoPackage com manguezais recortados para SC
- `Mapas_Gerados/mapa_manguezais_SC_GMW.png` — mapa estático com basemap
- `Mapas_Gerados/mapa_manguezais_SC_GMW.html` — mapa interativo (Folium)

Notas:

- Santa Catarina está no limite sul de distribuição de manguezais no Atlântico, portanto o recorte pode resultar em poucas ou nenhuma feição (dependendo da fonte e ano).
- Para uso oficial (licenciamento, relatórios), recomenda-se validar com ICMBio/MMA e MapBiomas.



 - (Em processamento) Mapa de manguezais de SC — GMW v3.0
- **Visualização:** Matplotlib, HTML/CSS

Scripts relevantes:

- `processar_manguezais_oficiais.py` — processa um vetor oficial (ICMBio/MapBiomas/GMW) indicado pelo usuário e gera PNG/HTML/GPKG
- `processar_gmw_manguezais.py` — baixa o GMW v3.0 e executa o recorte para SC automaticamente

## ▶️ Como reproduzir os mapas de manguezais

Pré-requisitos: ambiente Python ativado (pasta `.venv/`), pacotes já instalados.

PowerShell (Windows):

1) Usando um arquivo oficial (ICMBio/MapBiomas/GMW) já baixado

```
& ".venv/Scripts/python.exe" "processar_manguezais_oficiais.py" --fonte "C:/caminho/para/manguezais_oficial.shp"
```

2) Baixando automaticamente o Global Mangrove Watch (GMW v3.0) e processando

```
& ".venv/Scripts/python.exe" "processar_gmw_manguezais.py"
```

Saídas (diretório `Mapas_Gerados/`):
- `manguezais_sc_oficial.gpkg` ou `manguezais_sc_gmw.gpkg`
- `mapa_manguezais_SC_oficial.png` ou `mapa_manguezais_SC_GMW.png`
- `mapa_manguezais_SC_oficial.html` ou `mapa_manguezais_SC_GMW.html`

Troubleshooting:
- Se o serviço WFS do IBGE estiver indisponível, o script usará um limite aproximado de SC (bbox). Isso não altera o recorte final de forma relevante para a escala estadual.
- O download do GMW é grande (~2GB); se preferir, forneça um vetor oficial menor com `--fonte`.
```
.
├── Apresentacao_Projeto_Mestrado_Publica.html  # 🌐 Apresentação principal (pública)
├── Mapas_Gerados/                              # 🗺️ Mapas estáticos e interativos
├── Documentacao_Areas_Estudo.md                # 📄 Documentação detalhada
├── Bibliografia_Biodiversidade_Invasoes.md     # 📚 Referências bibliográficas
├── Checklist_Candidatura_Mestrado_2026.md      # ✅ Guia de candidatura
└── Scripts Python                              # 🐍 Análises e visualizações
```

## 📖 Documentos

- [Documentação das Áreas de Estudo](Documentacao_Areas_Estudo.md)
- [Bibliografia Especializada](Bibliografia_Biodiversidade_Invasoes.md)
- [Resumo de Dados Geoespaciais](Resumo_Dados_Geoespaciais.md)
- [Checklist de Candidatura](Checklist_Candidatura_Mestrado_2026.md)

## 🗺️ Mapas

Mapas gerados com dados geoespaciais oficiais:
- Mapa completo das 3 áreas
- Mapas individuais de cada ilha
- Mapa comparativo de escalas
- Mapa interativo HTML

## 📅 Timeline

- **Novembro 2025:** Preparação da candidatura
- **Março 2026:** Início previsto do mestrado
- **Março 2028:** Defesa prevista

## 📧 Contato

**Candidato:** Caetano Ronan  
**Instituição:** Universidade Federal de Santa Catarina (UFSC)  
**Programa:** PPGOceano - Programa de Pós-graduação em Oceanografia (UFSC)

---

<p align="center">
  <em>Gerado com dados reais e bibliografia científica atualizada</em><br>
  <em>Novembro de 2025</em>
</p>
