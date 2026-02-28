# Americas_Techguard

O Americas TechGuard tem como objetivo estruturar soluções tecnológicas aplicadas ao
monitoramento, prevenção e resposta a desastres climáticos, integrando dados ambientais,
sensoriamento remoto e análise geoespacial.

---

## Objetivo do Módulo NDVI

O módulo `ndvi_analysis` realiza:

- Cálculo do NDVI a partir de imagem multiespectral (bandas RED e NIR)
- Geração de mapa NDVI
- Geração de histograma dos valores
- Classificação temática da vegetação
- Aplicação de filtro mediano para suavização

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
    └── ndvi_analysis/
        ├── images/
        ├── notebook/
        ├── outputs/
        └── scripts/
            ├── ndvi_processing.py
            ├── ndvi_comparacao.py
            ├── ndvi_sazonalidade.py
            └── ndvi_metricas.py
```

## Requisitos

- Python 3.9 ou superior
- Dependências listadas em `requerimentos.txt`


## Instalação

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