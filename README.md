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
- Dependências listadas em `requirements.txt`


## Instalação

Clone o repositório e, na raiz do projeto, execute:

```bash
pip install -r requirements.txt
``` 
## Como Executar

Na raiz do projeto, execute:

```bash
python modules/ndvi_analysis/scripts/ndvi_processing.py
```