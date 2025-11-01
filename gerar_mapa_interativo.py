"""
Script para gerar apenas o mapa interativo HTML
"""

import geopandas as gpd
import folium
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def criar_mapa_interativo(gdfs, titulos, nome_arquivo):
    """
    Cria um mapa interativo em HTML usando Folium
    """
    print(f"\n🌐 Gerando mapa interativo HTML")
    
    # Calcular centro do mapa
    all_centroids = []
    for gdf in gdfs:
        gdf_wgs = gdf.to_crs(epsg=4326)
        centroid = gdf_wgs.geometry.centroid.iloc[0]
        all_centroids.append([centroid.y, centroid.x])
    
    center_lat = sum([c[0] for c in all_centroids]) / len(all_centroids)
    center_lon = sum([c[1] for c in all_centroids]) / len(all_centroids)
    
    # Criar mapa base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Adicionar camadas de tiles alternativas
    folium.TileLayer('CartoDB positron', name='Claro').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Escuro').add_to(m)
    
    # Cores
    cores = ['red', 'blue', 'green']
    
    # Adicionar cada área
    for gdf, titulo, cor in zip(gdfs, titulos, cores):
        gdf_wgs = gdf.to_crs(epsg=4326)
        
        # Calcular informações
        area_ha = gdf.geometry.area.sum() / 10000
        centroid = gdf_wgs.geometry.centroid.iloc[0]
        
        # Adicionar polígono
        folium.GeoJson(
            gdf_wgs.geometry.__geo_interface__,
            name=titulo,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': 'darkblue',
                'weight': 2,
                'fillOpacity': 0.4
            },
            tooltip=f"{titulo}: {area_ha:.2f} ha"
        ).add_to(m)
        
        # Adicionar marcador
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=folium.Popup(
                f"<b>{titulo}</b><br>"
                f"Área: {area_ha:.2f} ha<br>"
                f"Lat: {abs(centroid.y):.4f}°S<br>"
                f"Lon: {abs(centroid.x):.4f}°W",
                max_width=200
            ),
            icon=folium.Icon(color=cor, icon='info-sign')
        ).add_to(m)
    
    # Adicionar controles
    folium.LayerControl().add_to(m)
    
    # Salvar
    m.save(nome_arquivo)
    print(f"  ✅ Salvo: {nome_arquivo}")

# Carregar dados
base_path = Path(r"C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Projeto Mestrado")
mapas_path = base_path / "Projeto_mestrado" / "Mapas"
output_path = base_path / "Mapas_Gerados"

arquivos = [
    mapas_path / "REBIO_Arvoredo.gpkg",
    mapas_path / "Ilha_Campeche.gpkg",
    mapas_path / "Ilha_Xavier.gpkg"
]

titulos = [
    "REBIO Marinha do Arvoredo",
    "Ilha do Campeche",
    "Ilha Xavier"
]

gdfs = [gpd.read_file(arquivo) for arquivo in arquivos]

criar_mapa_interativo(gdfs, titulos, output_path / "mapa_interativo.html")
print("\n✅ Mapa interativo gerado! Abra o arquivo no navegador.")
