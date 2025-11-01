"""
Script para gerar mapas das áreas de estudo do projeto de mestrado
Autor: Caetano Ronan
Data: Novembro 2025

Gera:
1. Mapas individuais de cada ilha
2. Mapa conjunto das três áreas
3. Mapa de localização regional
4. Mapa interativo HTML
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import folium
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def criar_mapa_individual(gdf, titulo, nome_arquivo, cor='#2E86AB'):
    """
    Cria um mapa individual de uma área de estudo
    """
    print(f"\n📍 Gerando mapa: {titulo}")
    
    # Converter para Web Mercator para usar basemap
    gdf_web = gdf.to_crs(epsg=3857)
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plotar área
    gdf_web.plot(ax=ax, color=cor, alpha=0.6, edgecolor='darkblue', linewidth=2)
    
    # Adicionar basemap (OpenStreetMap)
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.8)
    except:
        print("  ⚠️  Basemap não disponível (sem conexão). Mapa sem fundo.")
    
    # Configurar título e labels
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    
    # Adicionar grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Adicionar informações
    area_ha = gdf.geometry.area.sum() / 10000  # converter m² para hectares
    centroid = gdf.to_crs(epsg=4326).geometry.centroid.iloc[0]
    
    info_text = f"Área: {area_ha:.2f} ha\nCentroide: {abs(centroid.y):.4f}°S, {abs(centroid.x):.4f}°W"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Adicionar seta do norte
    x, y, arrow_length = 0.95, 0.95, 0.08
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
                arrowprops=dict(facecolor='black', width=3, headwidth=8),
                ha='center', va='center', fontsize=14, fontweight='bold',
                xycoords=ax.transAxes)
    
    # Salvar
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"  ✅ Salvo: {nome_arquivo}")
    plt.close()

def criar_mapa_conjunto(gdfs, titulos, nome_arquivo):
    """
    Cria um mapa com todas as áreas juntas
    """
    print(f"\n🗺️  Gerando mapa conjunto das três áreas")
    
    cores = ['#E63946', '#2E86AB', '#06A77D']  # Vermelho, Azul, Verde
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Plotar cada área
    for gdf, titulo, cor in zip(gdfs, titulos, cores):
        gdf_web = gdf.to_crs(epsg=3857)
        gdf_web.plot(ax=ax, color=cor, alpha=0.6, edgecolor='darkblue', 
                     linewidth=1.5, label=titulo)
    
    # Adicionar basemap
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.7)
    except:
        print("  ⚠️  Basemap não disponível")
    
    # Configurar
    ax.set_title('Áreas de Estudo - Projeto de Mestrado', 
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Seta do norte
    x, y, arrow_length = 0.95, 0.95, 0.06
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
                arrowprops=dict(facecolor='black', width=3, headwidth=8),
                ha='center', va='center', fontsize=14, fontweight='bold',
                xycoords=ax.transAxes)
    
    # Salvar
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"  ✅ Salvo: {nome_arquivo}")
    plt.close()

def criar_mapa_comparativo(gdfs, titulos, nome_arquivo):
    """
    Cria figura com 3 subplots mostrando cada área individualmente
    """
    print(f"\n📊 Gerando mapa comparativo")
    
    cores = ['#E63946', '#2E86AB', '#06A77D']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for ax, gdf, titulo, cor in zip(axes, gdfs, titulos, cores):
        gdf_web = gdf.to_crs(epsg=3857)
        gdf_web.plot(ax=ax, color=cor, alpha=0.6, edgecolor='darkblue', linewidth=2)
        
        try:
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.7)
        except:
            pass
        
        ax.set_title(titulo, fontsize=13, fontweight='bold')
        ax.set_xlabel('Longitude', fontsize=9)
        ax.set_ylabel('Latitude', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Adicionar área
        area_ha = gdf.geometry.area.sum() / 10000
        ax.text(0.5, 0.02, f'Área: {area_ha:.2f} ha', 
                transform=ax.transAxes, ha='center',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=9)
    
    fig.suptitle('Comparação das Áreas de Estudo', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"  ✅ Salvo: {nome_arquivo}")
    plt.close()

def criar_mapa_interativo(gdfs, titulos, nome_arquivo):
    """
    Cria um mapa interativo em HTML usando Folium
    """
    print(f"\n🌐 Gerando mapa interativo HTML")
    
    # Calcular centro do mapa (média das coordenadas)
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
    
    # Adicionar camadas de tiles adicionais
    folium.TileLayer('Stamen Terrain', name='Terreno').add_to(m)
    folium.TileLayer('Stamen Toner', name='Preto e Branco').add_to(m)
    folium.TileLayer('CartoDB positron', name='Claro').add_to(m)
    
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
        
        # Adicionar marcador no centroide
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
    
    # Adicionar controle de camadas
    folium.LayerControl().add_to(m)
    
    # Adicionar escala
    folium.plugins.MeasureControl(position='topleft', 
                                   primary_length_unit='kilometers',
                                   secondary_length_unit='miles').add_to(m)
    
    # Adicionar mini mapa
    minimap = folium.plugins.MiniMap(toggle_display=True)
    m.add_child(minimap)
    
    # Salvar
    m.save(nome_arquivo)
    print(f"  ✅ Salvo: {nome_arquivo}")
    print(f"  📂 Abra o arquivo no navegador para visualizar")

def criar_mapa_escala_comparativa(gdfs, titulos, nome_arquivo):
    """
    Cria mapa mostrando as áreas na mesma escala para comparação de tamanho
    """
    print(f"\n📏 Gerando mapa de escala comparativa")
    
    cores = ['#E63946', '#2E86AB', '#06A77D']
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Plotar REBIO (maior) centralizada
    gdf_rebio = gdfs[0].to_crs(epsg=3857)
    rebio_centroid = gdf_rebio.geometry.centroid.iloc[0]
    
    gdf_rebio.plot(ax=ax, color=cores[0], alpha=0.3, edgecolor='darkred', 
                   linewidth=2, label=titulos[0])
    
    # Plotar outras ilhas deslocadas para visualização
    offset_x = gdf_rebio.total_bounds[2] - gdf_rebio.total_bounds[0]
    
    for i, (gdf, titulo, cor) in enumerate(zip(gdfs[1:], titulos[1:], cores[1:]), 1):
        gdf_web = gdf.to_crs(epsg=3857)
        
        # Deslocar geometria para o lado
        gdf_shifted = gdf_web.copy()
        gdf_shifted.geometry = gdf_shifted.translate(xoff=offset_x * i * 0.3, yoff=0)
        
        gdf_shifted.plot(ax=ax, color=cor, alpha=0.6, edgecolor='darkblue', 
                        linewidth=2, label=titulo)
    
    ax.set_title('Comparação de Tamanho das Áreas (Mesma Escala)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Distância relativa (metros)', fontsize=12)
    ax.set_ylabel('Distância relativa (metros)', fontsize=12)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    # Adicionar barra de escala manual
    ax.text(0.02, 0.02, '← 5 km →', transform=ax.transAxes,
            fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"  ✅ Salvo: {nome_arquivo}")
    plt.close()

def main():
    """
    Função principal
    """
    print("\n" + "="*80)
    print("GERAÇÃO DE MAPAS - PROJETO MESTRADO")
    print("="*80)
    
    # Definir caminhos
    base_path = Path(r"C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Projeto Mestrado")
    mapas_path = base_path / "Projeto_mestrado" / "Mapas"
    output_path = base_path / "Mapas_Gerados"
    
    # Criar pasta de saída
    output_path.mkdir(exist_ok=True)
    
    # Carregar dados
    print("\n📂 Carregando dados geoespaciais...")
    
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
    
    gdfs = []
    for arquivo, titulo in zip(arquivos, titulos):
        if arquivo.exists():
            gdf = gpd.read_file(arquivo)
            gdfs.append(gdf)
            print(f"  ✅ {titulo}: {len(gdf)} feature(s)")
        else:
            print(f"  ❌ Arquivo não encontrado: {arquivo.name}")
    
    if len(gdfs) != 3:
        print("\n❌ Erro: nem todos os arquivos foram carregados!")
        return
    
    # Gerar mapas individuais
    print("\n" + "="*80)
    print("1. MAPAS INDIVIDUAIS")
    print("="*80)
    
    cores_individuais = ['#E63946', '#2E86AB', '#06A77D']
    for gdf, titulo, cor in zip(gdfs, titulos, cores_individuais):
        nome_limpo = titulo.replace(" ", "_").replace("REBIO_", "").replace("Ilha_do_", "")
        criar_mapa_individual(
            gdf, 
            titulo, 
            output_path / f"mapa_{nome_limpo}.png",
            cor=cor
        )
    
    # Mapa conjunto
    print("\n" + "="*80)
    print("2. MAPA CONJUNTO")
    print("="*80)
    criar_mapa_conjunto(gdfs, titulos, output_path / "mapa_todas_areas.png")
    
    # Mapa comparativo
    print("\n" + "="*80)
    print("3. MAPA COMPARATIVO")
    print("="*80)
    criar_mapa_comparativo(gdfs, titulos, output_path / "mapa_comparativo.png")
    
    # Mapa de escala
    print("\n" + "="*80)
    print("4. MAPA DE ESCALA")
    print("="*80)
    criar_mapa_escala_comparativa(gdfs, titulos, output_path / "mapa_escala_comparativa.png")
    
    # Mapa interativo
    print("\n" + "="*80)
    print("5. MAPA INTERATIVO")
    print("="*80)
    criar_mapa_interativo(gdfs, titulos, output_path / "mapa_interativo.html")
    
    # Resumo final
    print("\n" + "="*80)
    print("✅ MAPAS GERADOS COM SUCESSO!")
    print("="*80)
    print(f"\n📁 Localização: {output_path}")
    print("\nArquivos gerados:")
    print("  1. mapa_Marinha_do_Arvoredo.png")
    print("  2. mapa_Campeche.png")
    print("  3. mapa_Xavier.png")
    print("  4. mapa_todas_areas.png")
    print("  5. mapa_comparativo.png")
    print("  6. mapa_escala_comparativa.png")
    print("  7. mapa_interativo.html (abra no navegador!)")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
