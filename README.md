# Modelo de Exposição Territorial ao Risco  
### Juiz de Fora – MG

---

## 📌 Visão Geral

Este projeto implementa um modelo geoespacial para identificação da exposição territorial ao risco físico em Juiz de Fora (MG), integrando:

- Suscetibilidade à inundação
- Suscetibilidade a movimento de massa
- Setores censitários do Censo 2022 (IBGE)

O resultado é um modelo estruturado que permite analisar a distribuição espacial do risco e gerar mapas interativos para apoio à tomada de decisão em cenários de emergência.

---

## 🎯 Objetivo

Construir um pipeline reprodutível capaz de:

- Consolidar camadas de risco geológico
- Identificar setores censitários afetados
- Calcular área exposta ao risco
- Classificar nível de risco por setor
- Gerar visualização interativa do território

---

## 🧠 Metodologia

O modelo segue as etapas abaixo:

1. Leitura das bases de suscetibilidade (CPRM)
2. Padronização das classes de risco
3. Conversão das classes para score numérico
4. União espacial das camadas de risco
5. Interseção com setores censitários (IBGE)
6. Projeção para sistema métrico (UTM 23S – EPSG:31983)
7. Cálculo da área afetada por setor
8. Agregação por setor censitário
9. Classificação final do nível de risco
10. Exportação em GeoJSON
11. Geração de mapa interativo (Folium)

---

## 📊 Variáveis Geradas

| Variável | Descrição |
|----------|------------|
| score_final | Maior nível de risco identificado no setor |
| area_afetada_m2 | Área total afetada dentro do setor |
| nivel_risco | Classificação textual do risco |
| CD_SETOR | Código do setor censitário |

Classificação aplicada:

- 0 → Sem risco mapeado
- 1 → Baixa
- 2 → Média
- 3 → Alta

---

## 🗂 Estrutura do Projeto