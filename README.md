# Americas_Techguard

O Americas TechGuard é uma plataforma de análise geoespacial voltada ao monitoramento, prevenção e resposta a desastres climáticos, integrando sensoriamento remoto, dados hidrológicos, modelos digitais de terreno e análise espacial para apoiar a tomada de decisão.

---

## Objetivo do Módulo NDVI

O módulo `ndvi_analysis` realiza:

- Cálculo do NDVI a partir de imagem multiespectral (bandas RED e NIR)
- Geração de mapa NDVI
- Geração de histograma dos valores
- Classificação temática da vegetação
- Aplicação de filtro mediano para suavização
- Cálculo de área de risco

## Objetivo do Módulo HAND

O modelo HAND (Height Above Nearest Drainage) calcula a altura relativa de cada ponto do terreno em relação ao curso d’água hidrologicamente conectado mais próximo.

Essa metodologia é amplamente utilizada para identificar áreas potencialmente sujeitas a inundação, permitindo a classificação espacial do risco com base na topografia local.

O módulo `hand` realiza:

- Download automático de limites municipais do IBGE
- Delimitação das ottobacias hidrográficas
- Geração do Modelo HAND (Height Above Nearest Drainage)
- Classificação de áreas suscetíveis à inundação
- Geração de mapas de risco de inundação

## Estrutura do Projeto

```
Americas_Techguard/
│
├── data/
│   └── Fort_Lauderdale_MSI_all_bands.tif
│
├── docs/
│
└── modules/
    ├── ndvi_analysis/
    │   ├── images/
    │   ├── notebook/
    │   ├── outputs/
    │   └── scripts/
    │       ├── ndvi_processing.py
    │       ├── ndvi_comparacao.py
    │       ├── ndvi_sazonalidade.py
    │       ├── ndvi_metricas.py
    │       ├── comparativo.py
    │       ├── compare_regions.py
    │       ├── flood_model.py
    │       ├── flood_comparison_model.py
    │       └── area_de_risco.py
    │        
    └── hand/
        ├── core
        │   ├── ibge.py
        │   ├── snirh.py
        │   ├── dem.py
        │   ├── hand.py
        │   └── risk.py
        ├── outputs_dem
        │   ├── dem_source.tif
        │   └── ibge_2023.zip
        ├── outputs_hand
        │   ├── hand_risk.png
        │   └── hand_risk.tif
        ├── pipeline
        │   └── hand_pipeline.py
        ├── visualization
        │   └── risk_plot.py
        └── main.py
        




```

## Requisitos

- Python 3.9 ou superior
- (modulo NDVI) Dependências listadas em `requerimentos.txt`
- (modulo HAND) Dependências listadas em `requeriments.txt`


## Instalação (módulo NDVI)

Clone o repositório e, na raiz do projeto, execute:

```bash
pip install -r requerimentos.txt
``` 
**Nota:** 
1. Os arquivos de dados geoespaciais (`.tif`) não estão incluídos no repositório GitHub devido ao tamanho.  
2. Para executar o módulo NDVI:
    - crie a pasta `data/` na raiz do projeto
    - coloque arquivo (`.tif`) compatível dentro dessa pasta. 
3. O arquivo geoespacial deve ter as bandas RED e NIR nas posições:
    - RED -> Banda 4
    - NIR -> Banda 8
4. O arquivo GeoTIFF deve ter resolução espacial em metros, para que os cálculos de área por classe sejam corretos.

> Esses arquivos são necessários para que o módulo calcule corretamente o NDVI e gere mapas e histogramas precisos.

## Como Executar

Na raiz do projeto:

### 1. Processamento básico de imagem satelital NDVI única

```bash
python modules/ndvi_analysis/scripts/ndvi_processing.py
```
### 2. Comparação entre datas e ΔNDVI por gráfico

```bash
python modules/ndvi_analysis/scripts/ndvi_comparacao.py
```
### 3. Extrair dados métricos do NDVI

O script gera métricas estatísticas e espaciais do NDVI, incluindo:

- Estatísticas descritivas (média, mediana, desvio padrão, variância, percentis P10, P75 e P90)
- Área por classe de cobertura (km² e %)
- Diferença NDVI entre datas (ΔNDVI), caso sejam fornecidas duas imagens

```bash
python modules/ndvi_analysis/scripts/ndvi_metricas.py
```
### 4. Comparação entre datas ΔNDVI por imagem

```bash
python modules/ndvi_analysis/scripts/ndvi_sazonalidade.py
```
### 5. Cálculo de área de risco

```bash
python modules/ndvi_analysis/scripts/area_de_risco.py
```
## Instalação (módulo HAND)

Clone o repositório e, na raiz do projeto, execute:

```bash
pip install -r requeriments.txt
``` 
**Nota:** 
1. Os arquivos de dados geoespaciais (`.tif`) não estão incluídos no repositório GitHub devido ao tamanho.  

## Como Executar

Na raiz do projeto:

### Geração automática de mapa de risco de inundação (HAND)

```bash
python modules/hand/main.py
```