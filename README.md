# Modelo de Exposição Territorial ao Risco  
### Juiz de Fora – MG

---

## 📌 Visão Geral

Este projeto implementa um modelo geoespacial para identificação da exposição territorial ao risco físico no município de Juiz de Fora (MG).

O modelo integra camadas de suscetibilidade geológica (inundação e movimento de massa) com setores censitários do Censo 2022 (IBGE), permitindo identificar quais áreas do território apresentam maior exposição ao risco.

O resultado é uma base consolidada por setor censitário, com cálculo da área afetada, classificação do nível de risco e geração de mapa interativo para visualização espacial.

---

## 🎯 Objetivo

Construir um pipeline reprodutível capaz de:

- Integrar diferentes camadas de risco geológico
- Identificar setores censitários expostos
- Calcular a área territorial afetada
- Classificar o nível de risco por setor
- Gerar visualização interativa para apoio à tomada de decisão

O modelo pode servir como base para análises de vulnerabilidade territorial, planejamento urbano e apoio à gestão de risco em cenários de emergência.

---

## 🧠 Metodologia

O modelo segue as seguintes etapas:

1. Leitura das bases de suscetibilidade (CPRM)
2. Padronização das classes de risco (Baixa, Média, Alta)
3. Conversão das classes para score numérico
4. União espacial das camadas de risco
5. Interseção com setores censitários (IBGE)
6. Projeção para sistema métrico (UTM 23S – EPSG:31983)
7. Cálculo da área afetada por setor
8. Agregação por setor censitário
9. Classificação final do nível de risco
10. Exportação do resultado em GeoJSON
11. Geração de mapa interativo com Folium

A classificação final considera o maior nível de risco identificado dentro de cada setor.

---

## 📊 Variáveis Geradas

O pipeline gera as seguintes variáveis consolidadas por setor censitário:

| Variável | Descrição |
|----------|------------|
| CD_SETOR | Código do setor censitário |
| score_final | Maior score de risco identificado no setor |
| area_afetada_m2 | Soma da área afetada dentro do setor (m²) |
| nivel_risco | Classificação textual do risco |

### Classificação aplicada

- 0 → Sem risco mapeado
- 1 → Baixa
- 2 → Média
- 3 → Alta

---

## 🗂 Estrutura do Projeto

```
ProjetoJuizDeFora/
│
├── src/
│   ├── pipeline_risco.py     # Pipeline principal de processamento
│   └── gerar_mapa.py         # Geração do mapa interativo
│
├── data/                     # Bases geoespaciais locais (não versionadas)
│   ├── geociencia/
│   └── suscetibilidade/
│
├── outputs/                  # Resultados gerados (GeoJSON e HTML)
│
├── requirements.txt
├── .gitignore
└── README.md
```

As bases geoespaciais não estão versionadas neste repositório.

---

## 🗺 Mapa Interativo

O script `gerar_mapa.py` gera o arquivo:

```
outputs/mapa_exposicao_risco.html
```

O mapa apresenta:

- Setores censitários coloridos por nível de risco
- Tooltip com informações consolidadas
- Visualização navegável e interativa

---

## ⚙️ Como Executar

### 1️⃣ Clonar repositório

```bash
git clone https://github.com/andre-anjob/juizdefora-risco-territorial.git
cd juizdefora-risco-territorial
```

### 2️⃣ Criar ambiente virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar pipeline

```bash
python src/pipeline_risco.py
```

### 5️⃣ Gerar mapa

```bash
python src/gerar_mapa.py
```

---

## 🛠 Tecnologias Utilizadas

- Python
- GeoPandas
- Shapely
- PyProj
- Fiona
- Folium
- IBGE – Censo 2022
- CPRM – Cartas de Suscetibilidade Geológica

---

## 📦 Dados Utilizados

- Setores censitários – IBGE (Censo 2022)
- Cartas de suscetibilidade geológica – CPRM

As bases geoespaciais devem ser armazenadas localmente na pasta `data/`.

---

## 🔍 Aplicações

Este modelo pode ser utilizado para:

- Apoio à gestão de risco e defesa civil
- Planejamento urbano
- Priorização territorial
- Análise de vulnerabilidade física
- Integração futura com indicadores socioeconômicos

---

## 🚀 Próximos Passos

- Integração com renda média por setor (IBGE)
- Índice composto de vulnerabilidade territorial
- Cálculo de exposição populacional
- Dashboard analítico
- Modelagem de priorização territorial

---

## 👤 Autor

**Andre Severo**  
Engenharia de Dados | Análise Territorial | Modelagem Espacial  

GitHub: https://github.com/andre-anjob