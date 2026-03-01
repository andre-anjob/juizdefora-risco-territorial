from pathlib import Path
import os
import geopandas as gpd
import pandas as pd


# ==================================================
# CONFIGURAÇÕES GERAIS
# ==================================================

os.environ["SHAPE_RESTORE_SHX"] = "YES"

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

PATH_INUNDACAO = DATA_DIR / "suscetibilidade" / "inundacao" / "inundacao_A.shp"
PATH_MOVIMENTO = DATA_DIR / "suscetibilidade" / "movimento_de_massa" / "movimento_de_Massa_A.shp"
PATH_SETORES = DATA_DIR / "geociencia" / "MG_setores_CD2022" / "MG_setores_CD2022.shp"


# ==================================================
# FUNÇÕES
# ==================================================

def carregar_dados():
    inundacao = gpd.read_file(PATH_INUNDACAO)
    movimento = gpd.read_file(PATH_MOVIMENTO)
    setores = gpd.read_file(PATH_SETORES)

    print("✔ Dados carregados")
    return inundacao, movimento, setores


def padronizar_geometria(inundacao, movimento, setores):
    inundacao = inundacao.to_crs(setores.crs)
    movimento = movimento.to_crs(setores.crs)

    inundacao = inundacao[inundacao.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
    movimento = movimento[movimento.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
    setores = setores[setores.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()

    return inundacao, movimento, setores


def normalizar_classe(valor):
    if valor == "Baixa":
        return "Baixa"
    elif valor in ["Média", "Médio"]:
        return "Media"
    elif valor == "Alta":
        return "Alta"
    else:
        return None


def aplicar_score(inundacao, movimento):
    mapa_score = {"Baixa": 1, "Media": 2, "Alta": 3}

    inundacao["classe_padrao"] = inundacao["CLASSE"].apply(normalizar_classe)
    movimento["classe_padrao"] = movimento["CLASSE"].apply(normalizar_classe)

    inundacao["score"] = inundacao["classe_padrao"].map(mapa_score)
    movimento["score"] = movimento["classe_padrao"].map(mapa_score)

    return inundacao, movimento


def unir_riscos(inundacao, movimento):
    risco_union = gpd.overlay(
        inundacao,
        movimento,
        how="union",
        keep_geom_type=False
    )

    risco_union = risco_union[
        risco_union.geometry.type.isin(["Polygon", "MultiPolygon"])
    ].copy()

    risco_union = risco_union.explode(index_parts=False)

    risco_union["score_final"] = risco_union[["score_1", "score_2"]].max(axis=1)

    return risco_union


def intersectar_setores(setores, risco_union):
    setores_risco = gpd.overlay(
        setores,
        risco_union,
        how="intersection"
    )

    # Projetar para CRS métrico
    setores_risco = setores_risco.to_crs(epsg=31983)

    setores_risco["area_afetada_m2"] = setores_risco.geometry.area

    return setores_risco


def agregar_por_setor(setores, setores_risco):
    resumo = (
        setores_risco
        .groupby("CD_SETOR")
        .agg({
            "score_final": "max",
            "area_afetada_m2": "sum"
        })
        .reset_index()
    )

    setores_final = setores.merge(
        resumo,
        on="CD_SETOR",
        how="left"
    )

    setores_final["score_final"] = setores_final["score_final"].fillna(0)
    setores_final["area_afetada_m2"] = setores_final["area_afetada_m2"].fillna(0)

    return setores_final


def classificar_nivel(score):
    if score == 0:
        return "Sem risco mapeado"
    elif score == 1:
        return "Baixa"
    elif score == 2:
        return "Media"
    elif score == 3:
        return "Alta"
    else:
        return "Indefinido"


def exportar_resultado(setores_final):
    OUTPUT_DIR.mkdir(exist_ok=True)

    setores_final["nivel_risco"] = setores_final["score_final"].apply(classificar_nivel)

    output_path = OUTPUT_DIR / "setores_risco_final.geojson"

    setores_final.to_file(output_path, driver="GeoJSON")

    print("✔ Pipeline concluído com sucesso")
    print(f"Arquivo salvo em: {output_path}")


# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================

def main():
    inundacao, movimento, setores = carregar_dados()

    inundacao, movimento, setores = padronizar_geometria(
        inundacao, movimento, setores
    )

    inundacao, movimento = aplicar_score(inundacao, movimento)

    risco_union = unir_riscos(inundacao, movimento)

    setores_risco = intersectar_setores(setores, risco_union)

    setores_final = agregar_por_setor(setores, setores_risco)

    exportar_resultado(setores_final)


if __name__ == "__main__":
    main()