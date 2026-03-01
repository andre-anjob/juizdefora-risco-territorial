from pathlib import Path
import geopandas as gpd
import folium


# ==============================
# CAMINHOS
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

PATH_GEOJSON = OUTPUT_DIR / "setores_risco_final.geojson"
PATH_MAPA = OUTPUT_DIR / "mapa_exposicao_risco.html"


# ==============================
# FUNÇÕES
# ==============================

def carregar_dados():
    """Lê o GeoJSON gerado pelo pipeline"""
    setores = gpd.read_file(PATH_GEOJSON)
    return setores


def definir_cor(nivel):
    """Define cor por nível de risco"""
    if nivel == "Alta":
        return "red"
    elif nivel == "Media":
        return "orange"
    elif nivel == "Baixa":
        return "yellow"
    return "green"


def gerar_mapa(setores):
    """Gera mapa interativo"""
    setores = setores.to_crs(epsg=4326)

    centro = setores.geometry.centroid.unary_union.centroid

    mapa = folium.Map(
        location=[centro.y, centro.x],
        zoom_start=12
    )

    folium.GeoJson(
        setores,
        style_function=lambda feature: {
            "fillColor": definir_cor(feature["properties"]["nivel_risco"]),
            "color": "black",
            "weight": 0.3,
            "fillOpacity": 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["CD_SETOR", "nivel_risco", "area_afetada_m2"],
            aliases=["Setor:", "Nível:", "Área afetada (m²):"]
        )
    ).add_to(mapa)

    mapa.save(PATH_MAPA)

    print("Mapa gerado com sucesso")
    print(f"Arquivo salvo em: {PATH_MAPA}")


# ==============================
# EXECUÇÃO
# ==============================

def main():
    setores = carregar_dados()
    gerar_mapa(setores)


if __name__ == "__main__":
    main()