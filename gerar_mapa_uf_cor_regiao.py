from pathlib import Path
import base64
import geopandas as gpd
import folium

root = Path(r"c:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Projeto Mestrado")
uf = gpd.read_file(root / "Mapas_Gerados" / "manguezais_por_uf.gpkg", layer="manguezais_uf").to_crs(4326)

uf_diss = (
    uf[["UF", "regiao", "area_ha", "geometry"]]
    .dissolve(by=["UF", "regiao"], aggfunc="sum")
    .reset_index()
)

colors = {
    "Norte": "#1f78b4",
    "Nordeste": "#e31a1c",
    "Sudeste": "#6a3d9a",
    "Sul": "#33a02c",
}

regioes_ordem = ["Norte", "Nordeste", "Sudeste", "Sul"]

center = uf_diss.union_all().centroid
minx, miny, maxx, maxy = uf_diss.total_bounds
bounds = [[miny, minx], [maxy, maxx]]

m = folium.Map(
    location=[center.y, center.x],
    zoom_start=5,
    min_zoom=4,
    max_zoom=7,
    max_bounds=True,
    tiles=None,
)

m.fit_bounds(bounds)

folium.TileLayer(
    tiles="https://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
    attr="Google",
    name="Google Terrain",
    max_zoom=20,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
    show=True,
).add_to(m)
folium.TileLayer("OpenStreetMap", name="OpenStreetMap", show=False).add_to(m)

for regiao in regioes_ordem:
    color = colors[regiao]
    subset = uf_diss[uf_diss["regiao"] == regiao]

    group = folium.FeatureGroup(name=regiao, show=True)
    if subset.empty:
        folium.GeoJson(
            {"type": "FeatureCollection", "features": []},
            name=f"Sem dados: {regiao}",
        ).add_to(group)
    else:
        folium.GeoJson(
            subset.__geo_interface__,
            style_function=lambda f, c=color: {
                "fillColor": c,
                "color": "#111111",
                "weight": 1.6,
                "fillOpacity": 0.9,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["UF", "regiao", "area_ha"],
                aliases=["UF", "Região", "Área (ha)"],
                localize=True,
                labels=True,
                sticky=True,
            ),
        ).add_to(group)
    group.add_to(m)

titulo = """
<div style="position: fixed; top: 12px; left: 50%; transform: translateX(-50%); z-index: 9999;
                        background: rgba(255,255,255,0.96); border: 1px solid #cfcfcf; border-radius: 10px;
                        padding: 10px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); text-align: center;
                        min-width: 420px; max-width: 80%;">
    <div style="font-size: 20px; font-weight: 700; color: #1f2937;">Distribuição Geográfica dos Manguezais Brasileiros</div>
    <div style="font-size: 12px; color: #4b5563; margin-top: 2px;">Manguezais por unidade federativa com cores por macrorregião</div>
</div>
"""
m.get_root().html.add_child(folium.Element(titulo))

legend = """
<div style="position: fixed; bottom: 20px; left: 20px; z-index: 9999;
            background: white; border: 1px solid #ccc; border-radius: 6px;
            padding: 10px; font-size: 12px;">
  <span style="display:inline-block;width:10px;height:10px;background:#1f78b4;margin-right:6px;"></span>Norte<br>
  <span style="display:inline-block;width:10px;height:10px;background:#e31a1c;margin-right:6px;"></span>Nordeste<br>
  <span style="display:inline-block;width:10px;height:10px;background:#6a3d9a;margin-right:6px;"></span>Sudeste<br>
  <span style="display:inline-block;width:10px;height:10px;background:#33a02c;margin-right:6px;"></span>Sul
</div>
"""
m.get_root().html.add_child(folium.Element(legend))

rosa_ventos_path = root / "_tmp_icmbio" / "rosa_ventos.png"
rosa_b64 = base64.b64encode(rosa_ventos_path.read_bytes()).decode()
rosa_ventos = f"""
<div style="position: fixed; top: 110px; left: 10px; z-index: 9999;
            width: 92px; height: 92px; background: rgba(255,255,255,0.92);
            border: 1px solid #cfcfcf; border-radius: 8px;
            display:flex; align-items:center; justify-content:center;">
  <img src="data:image/png;base64,{rosa_b64}" style="width:80px;height:80px;object-fit:contain;" alt="Rosa dos Ventos"/>
</div>
"""
m.get_root().html.add_child(folium.Element(rosa_ventos))

rodape = """
<div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 9999;
                        background: rgba(255,255,255,0.93); border-top: 1px solid #ccc;
                        padding: 5px 16px; font-size: 11px; color: #333;
                        display: flex; gap: 24px; align-items: center;">
    <span><b>Autor:</b> Ronan Caetano</span>
    <span><b>Ano:</b> 2026</span>
    <span><b>Fonte dos dados:</b> ICMBio / IBGE</span>
    <span><b>Projeção:</b> SIRGAS 2000 (EPSG 4674)</span>
</div>
"""
m.get_root().html.add_child(folium.Element(rodape))

folium.LayerControl(collapsed=False).add_to(m)
out = root / "Mapas_Gerados" / "mapa_manguezais_por_uf_cor_regiao.html"
m.save(out)

print("HTML", out)
print("UFs", len(uf_diss))
