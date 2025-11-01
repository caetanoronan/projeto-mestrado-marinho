"""
Script para extrair informações dos arquivos geoespaciais do projeto de mestrado
Autor: Caetano Ronan
Data: Novembro 2025
"""

import geopandas as gpd
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analisar_gpkg(caminho_arquivo):
    """
    Analisa um arquivo GeoPackage e extrai informações relevantes
    """
    print(f"\n{'='*80}")
    print(f"Analisando: {os.path.basename(caminho_arquivo)}")
    print(f"{'='*80}")
    
    try:
        # Ler o arquivo
        gdf = gpd.read_file(caminho_arquivo)
        
        # Informações básicas
        print(f"\n📊 INFORMAÇÕES GERAIS:")
        print(f"   • Número de features: {len(gdf)}")
        print(f"   • Sistema de Coordenadas: {gdf.crs}")
        print(f"   • Tipo de geometria: {gdf.geometry.type.unique()}")
        
        # Colunas/atributos
        print(f"\n📋 ATRIBUTOS/COLUNAS:")
        for col in gdf.columns:
            if col != 'geometry':
                print(f"   • {col}: {gdf[col].dtype}")
        
        # Reprojetar para WGS84 (lat/lon) se necessário
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf_wgs84 = gdf.to_crs(epsg=4326)
        else:
            gdf_wgs84 = gdf
        
        # Coordenadas (centroide e bounds)
        print(f"\n📍 COORDENADAS (WGS84 - Lat/Lon):")
        bounds = gdf_wgs84.total_bounds
        print(f"   • Longitude mínima: {bounds[0]:.6f}°")
        print(f"   • Latitude mínima: {bounds[1]:.6f}°")
        print(f"   • Longitude máxima: {bounds[2]:.6f}°")
        print(f"   • Latitude máxima: {bounds[3]:.6f}°")
        
        centroid = gdf_wgs84.geometry.unary_union.centroid
        print(f"   • Centroide: {centroid.y:.6f}°S, {abs(centroid.x):.6f}°W")
        
        # Calcular área se for polígono
        if any(gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])):
            # Reprojetar para UTM para cálculo de área preciso
            # UTM Zone 22S para Santa Catarina
            gdf_utm = gdf.to_crs(epsg=32722)
            area_m2 = gdf_utm.geometry.area.sum()
            area_km2 = area_m2 / 1_000_000
            area_hectares = area_m2 / 10_000
            
            print(f"\n📏 ÁREA:")
            print(f"   • {area_m2:.2f} m²")
            print(f"   • {area_hectares:.2f} hectares")
            print(f"   • {area_km2:.4f} km²")
        
        # Calcular comprimento se for linha
        if any(gdf.geometry.type.isin(['LineString', 'MultiLineString'])):
            gdf_utm = gdf.to_crs(epsg=32722)
            comprimento_m = gdf_utm.geometry.length.sum()
            comprimento_km = comprimento_m / 1000
            
            print(f"\n📏 COMPRIMENTO:")
            print(f"   • {comprimento_m:.2f} m")
            print(f"   • {comprimento_km:.2f} km")
        
        # Mostrar primeiras linhas de dados
        if len(gdf) > 0:
            print(f"\n📄 PRIMEIRAS LINHAS DE DADOS:")
            # Excluir coluna geometry para melhor visualização
            cols_to_show = [col for col in gdf.columns if col != 'geometry']
            if cols_to_show:
                print(gdf[cols_to_show].head())
        
        return {
            'nome': os.path.basename(caminho_arquivo),
            'features': len(gdf),
            'crs': str(gdf.crs),
            'centroid_lat': centroid.y,
            'centroid_lon': centroid.x,
            'bounds': bounds,
            'area_hectares': area_hectares if any(gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])) else None
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        return None

def analisar_kml(caminho_arquivo):
    """
    Analisa um arquivo KML
    """
    print(f"\n{'='*80}")
    print(f"Analisando: {os.path.basename(caminho_arquivo)}")
    print(f"{'='*80}")
    
    try:
        # Habilitar driver KML do Fiona
        import fiona
        fiona.drvsupport.supported_drivers['KML'] = 'rw'
        
        # Ler o arquivo KML
        gdf = gpd.read_file(caminho_arquivo, driver='KML')
        
        # Informações básicas
        print(f"\n📊 INFORMAÇÕES GERAIS:")
        print(f"   • Número de features: {len(gdf)}")
        print(f"   • Sistema de Coordenadas: {gdf.crs}")
        print(f"   • Tipo de geometria: {gdf.geometry.type.unique()}")
        
        # Colunas/atributos
        print(f"\n📋 ATRIBUTOS/COLUNAS:")
        for col in gdf.columns:
            if col != 'geometry':
                print(f"   • {col}")
                # Mostrar valores únicos se houver poucos
                unique_vals = gdf[col].unique()
                if len(unique_vals) <= 5:
                    print(f"     Valores: {unique_vals}")
        
        # Coordenadas (o KML já está em WGS84)
        print(f"\n📍 COORDENADAS (WGS84 - Lat/Lon):")
        bounds = gdf.total_bounds
        print(f"   • Longitude mínima: {bounds[0]:.6f}°")
        print(f"   • Latitude mínima: {bounds[1]:.6f}°")
        print(f"   • Longitude máxima: {bounds[2]:.6f}°")
        print(f"   • Latitude máxima: {bounds[3]:.6f}°")
        
        centroid = gdf.geometry.unary_union.centroid
        print(f"   • Centroide: {centroid.y:.6f}°S, {abs(centroid.x):.6f}°W")
        
        # Calcular área se for polígono
        if any(gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])):
            gdf_utm = gdf.to_crs(epsg=32722)
            area_m2 = gdf_utm.geometry.area.sum()
            area_km2 = area_m2 / 1_000_000
            area_hectares = area_m2 / 10_000
            
            print(f"\n📏 ÁREA:")
            print(f"   • {area_m2:.2f} m²")
            print(f"   • {area_hectares:.2f} hectares")
            print(f"   • {area_km2:.4f} km²")
        
        # Mostrar dados
        if len(gdf) > 0:
            print(f"\n📄 DADOS:")
            cols_to_show = [col for col in gdf.columns if col != 'geometry']
            if cols_to_show:
                print(gdf[cols_to_show].head())
        
        return {
            'nome': os.path.basename(caminho_arquivo),
            'features': len(gdf),
            'centroid_lat': centroid.y,
            'centroid_lon': centroid.x,
            'bounds': bounds,
            'area_hectares': area_hectares if any(gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])) else None
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo KML: {str(e)}")
        return None

def main():
    """
    Função principal
    """
    print("\n" + "="*80)
    print("ANÁLISE DE DADOS GEOESPACIAIS - PROJETO MESTRADO")
    print("="*80)
    
    # Definir caminhos
    base_path = Path(r"C:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Projeto Mestrado")
    mapas_path = base_path / "Projeto_mestrado" / "Mapas"
    
    # Lista de arquivos para processar
    arquivos_gpkg = [
        mapas_path / "Ilha_Campeche.gpkg",
        mapas_path / "Ilha_Xavier.gpkg",
        mapas_path / "REBIO_Arvoredo.gpkg",
        mapas_path / "Projeto_mapas_mestrado.gpkg"
    ]
    
    arquivo_kml = base_path / "Projeto_mestrado" / "rebio_marinha_do_arvoredo.kml"
    
    resultados = []
    
    # Processar GeoPackages
    print("\n\n🗺️  PROCESSANDO ARQUIVOS GEOPACKAGE (.gpkg)")
    print("="*80)
    
    for arquivo in arquivos_gpkg:
        if arquivo.exists():
            resultado = analisar_gpkg(str(arquivo))
            if resultado:
                resultados.append(resultado)
        else:
            print(f"\n⚠️  Arquivo não encontrado: {arquivo.name}")
    
    # Processar KML
    print("\n\n🌍 PROCESSANDO ARQUIVO KML")
    print("="*80)
    
    if arquivo_kml.exists():
        resultado = analisar_kml(str(arquivo_kml))
        if resultado:
            resultados.append(resultado)
    else:
        print(f"\n⚠️  Arquivo não encontrado: {arquivo_kml.name}")
    
    # Resumo final
    print("\n\n" + "="*80)
    print("📊 RESUMO FINAL")
    print("="*80)
    
    for res in resultados:
        if res:
            print(f"\n{res['nome']}:")
            print(f"   • Features: {res['features']}")
            print(f"   • Centroide: {res['centroid_lat']:.6f}°S, {abs(res['centroid_lon']):.6f}°W")
            if res['area_hectares']:
                print(f"   • Área: {res['area_hectares']:.2f} hectares")
    
    print("\n" + "="*80)
    print("✅ Análise concluída!")
    print("="*80)

if __name__ == "__main__":
    main()
