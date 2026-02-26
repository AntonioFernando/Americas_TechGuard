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
            └── ndvi_processing.py
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
    - coloque o arquivo `Fort_Lauderdale_MSI_all_bands.tif`, ou qualquer outro arquivo (`.tif`) compatível dentro dessa pasta. 
3. O arquivo geoespacial deve ter as bandas RED e NIR nas posições:
    - RED -> Banda 4
    - NIR -> Banda 8

> Esses arquivos são necessários para que o módulo calcule corretamente o NDVI e gere mapas e histogramas precisos.

## Como Executar

Na raiz do projeto, execute:

```bash
python modules/ndvi_analysis/scripts/ndvi_processing.py
```