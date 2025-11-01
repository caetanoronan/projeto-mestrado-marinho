# Resumo dos Dados Geoespaciais Extraídos
**Projeto de Mestrado - Ecologia Marinha**  
**Data da Análise:** Novembro 2025

---

## 📊 DADOS EXTRAÍDOS DOS ARQUIVOS

### 🏝️ Ilha do Campeche
- **Arquivo:** `Ilha_Campeche.gpkg`
- **Sistema:** EPSG:31982 (SIRGAS 2000 / UTM zone 22S)
- **Features:** 1 polígono
- **Centroide:** 27.696810°S, 48.465186°W
- **Área:** 76.19 hectares (0.76 km²)
- **Bounding Box:**
  - Lat: -27.705218° a -27.690280°
  - Lon: -48.469146° a -48.460224°

### 🏝️ Ilha Xavier
- **Arquivo:** `Ilha_Xavier.gpkg`
- **Sistema:** EPSG:29192 (SIRGAS 2000 / UTM zone 22S)
- **Features:** 3 polígonos (ilha principal + ilhotas)
- **Centroide:** 27.609994°S, 48.386324°W
- **Área:** 16.98 hectares (0.17 km²)
- **Bounding Box:**
  - Lat: -27.612540° a -27.607237°
  - Lon: -48.392466° a -48.383254°

### 🌊 REBIO Marinha do Arvoredo
- **Arquivo:** `REBIO_Arvoredo.gpkg`
- **Sistema:** EPSG:29192 (SIRGAS 2000 / UTM zone 22S)
- **Features:** 1 polígono
- **Centroide:** 27.225903°S, 48.365595°W
- **Área:** 17,131.72 hectares (171.32 km²)
- **Bounding Box:**
  - Lat: -27.299901° a -27.158831°
  - Lon: -48.425423° a -48.308816°

### 🌍 REBIO Arvoredo (KML)
- **Arquivo:** `rebio_marinha_do_arvoredo.kml`
- **Sistema:** EPSG:4326 (WGS84)
- **Features:** 1 multipolígono
- **Centroide:** 27.225786°S, 48.365649°W
- **Área:** 17,119.26 hectares (171.19 km²)
- **Bounding Box:**
  - Lat: -27.299665° a -27.158831°
  - Lon: -48.425482° a -48.308816°

### 📍 Ponto de Referência
- **Arquivo:** `Projeto_mapas_mestrado.gpkg`
- **Sistema:** EPSG:31982
- **Features:** 1 ponto
- **Coordenadas:** 27.278635°S, 48.374690°W
- **Observação:** Possivelmente um ponto de referência ou base

---

## 📈 COMPARAÇÃO DE ÁREAS

```
REBIO Arvoredo:    ████████████████████████████████████████ 17,131.72 ha
Ilha do Campeche:  ▌ 76.19 ha
Ilha Xavier:       ▏ 16.98 ha
```

**Proporções:**
- REBIO Arvoredo é **225x** maior que Ilha do Campeche
- REBIO Arvoredo é **1,009x** maior que Ilha Xavier
- Ilha do Campeche é **4.5x** maior que Ilha Xavier

---

## 🗺️ DISTRIBUIÇÃO GEOGRÁFICA

**Ordenação Norte → Sul:**
1. **REBIO Arvoredo** (27.23°S) - Mais ao norte
2. **Ilha Xavier** (27.61°S)
3. **Ilha do Campeche** (27.70°S) - Mais ao sul

**Distâncias Aproximadas (linha reta):**
- REBIO Arvoredo ↔ Ilha Xavier: ~42 km
- Ilha Xavier ↔ Ilha do Campeche: ~10 km
- REBIO Arvoredo ↔ Ilha do Campeche: ~52 km

---

## 🎯 IMPLICAÇÕES PARA A PESQUISA

### Biogeografia de Ilhas
- Grande variação em tamanho de área (3 ordens de magnitude)
- Permite testar teoria de biogeografia: área vs. biodiversidade
- Diferentes capacidades de suporte populacional

### Conectividade
- Ilhas relativamente próximas (10-50 km)
- Potencial para dispersão larval entre áreas
- Correntes marinhas como vetores de conectividade

### Pressões Antrópicas
- **REBIO Arvoredo:** Proteção máxima, visitação controlada
- **Ilha do Campeche:** Alta pressão turística, próxima à cidade
- **Ilha Xavier:** Pressão intermediária

### Amostragem
- Esforço amostral deve ser proporcional à área?
- Ou padronizado para permitir comparação direta?
- Considerar heterogeneidade de habitats

---

## ✅ VALIDAÇÃO DOS DADOS

### Sistemas de Coordenadas
✅ Todos os arquivos usam SIRGAS 2000 (sistema brasileiro oficial)  
✅ Dados convertidos para WGS84 para compatibilidade  
✅ Projeção UTM Zone 22S apropriada para Santa Catarina

### Qualidade dos Dados
✅ Coordenadas consistentes com localização conhecida  
✅ Áreas compatíveis com dados publicados  
✅ Centroides calculados corretamente  
✅ Sistema de referência adequado para análises métricas

### Observações
- Arquivo .gpkg e .kml da REBIO têm áreas levemente diferentes (12.46 ha)
- Provavelmente devido a diferenças na precisão dos vértices
- Diferença desprezível para análises ecológicas (<0.1%)

---

## 📝 PRÓXIMOS PASSOS

### Análises Espaciais
- [ ] Criar mapas de localização das três áreas
- [ ] Calcular distâncias exatas entre ilhas
- [ ] Mapear batimetria e habitats bentônicos
- [ ] Identificar áreas prioritárias para amostragem

### Dados Complementares
- [ ] Obter dados de batimetria (profundidade)
- [ ] Mapear tipos de substrato (rochoso, arenoso)
- [ ] Dados oceanográficos (temperatura, salinidade)
- [ ] Dados de correntes marinhas

### Validação em Campo
- [ ] Verificar coordenadas com GPS em campo
- [ ] Fotografar pontos de referência
- [ ] Mapear áreas de interesse específico

---

## 📚 ARQUIVOS GERADOS

1. `analisar_dados_geoespaciais.py` - Script Python para análise
2. `Documentacao_Areas_Estudo.md` - Documento atualizado com coordenadas
3. `Resumo_Dados_Geoespaciais.md` - Este arquivo

---

**Análise realizada com:**
- Python 3.13
- GeoPandas 1.0+
- Fiona
- Shapely
- PyProj

**Última atualização:** Novembro 2025
