from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def format_ha(value: float) -> str:
		return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_int(value: int) -> str:
		return f"{value:,}".replace(",", ".")


def fig_html(fig: go.Figure, include_js: bool = False) -> str:
		return fig.to_html(
				full_html=False,
				include_plotlyjs="cdn" if include_js else False,
				config={"displayModeBar": False, "responsive": True},
		)


root = Path(r"c:\Users\caetanoronan\OneDrive - UFSC\Área de Trabalho\Projeto Mestrado")
out_dir = root / "Mapas_Gerados"

df_reg = pd.read_csv(out_dir / "manguezais_por_regiao.csv")
df_uf = pd.read_csv(out_dir / "manguezais_por_uf.csv")

colors = {
		"Norte": "#1f78b4",
		"Nordeste": "#e31a1c",
		"Sudeste": "#6a3d9a",
		"Sul": "#33a02c",
}

ordem = ["Norte", "Nordeste", "Sudeste", "Sul"]
order_map = {regiao: i for i, regiao in enumerate(ordem)}

df_reg["ordem"] = df_reg["regiao"].map(order_map)
df_reg = df_reg.sort_values("ordem").drop(columns="ordem")

df_uf["ordem"] = df_uf["regiao"].map(order_map)
df_uf = df_uf.sort_values(["ordem", "area_ha"], ascending=[True, False]).drop(columns="ordem")

total_area = df_reg["area_ha"].sum()
total_regioes = len(df_reg)
total_ufs = len(df_uf)
media_regional = total_area / total_regioes

df_reg["percentual"] = df_reg["area_ha"] / total_area * 100
df_uf["percentual_nacional"] = df_uf["area_ha"] / total_area * 100
df_uf["area_label"] = df_uf["area_ha"].map(lambda value: f"{format_ha(value)} ha")

maior_regiao = df_reg.sort_values("area_ha", ascending=False).iloc[0]
maior_uf = df_uf.sort_values("area_ha", ascending=False).iloc[0]

reg_summary = (
		df_uf.groupby("regiao", as_index=False)
		.agg(
				ufs=("UF", "count"),
				area_total=("area_ha", "sum"),
				media_uf=("area_ha", "mean"),
		)
)
reg_summary["percentual"] = reg_summary["area_total"] / total_area * 100
reg_summary["maior_uf"] = reg_summary["regiao"].map(
		df_uf.sort_values("area_ha", ascending=False).groupby("regiao")["UF"].first()
)
reg_summary["ordem"] = reg_summary["regiao"].map(order_map)
reg_summary = reg_summary.sort_values("ordem").drop(columns="ordem")

fig_bar = px.bar(
		df_reg,
		x="regiao",
		y="area_ha",
		color="regiao",
		color_discrete_map=colors,
		text=df_reg["area_ha"].map(lambda v: f"{format_ha(v)} ha"),
		category_orders={"regiao": ordem},
)
fig_bar.update_traces(
		hovertemplate="<b>%{x}</b><br>Área: %{y:,.2f} ha<extra></extra>",
		textposition="outside",
		cliponaxis=False,
)
fig_bar.update_layout(
		title="📊 Área de manguezais por região",
		paper_bgcolor="white",
		plot_bgcolor="white",
		margin=dict(l=20, r=20, t=56, b=20),
		yaxis_title="Área (ha)",
		xaxis_title="",
		showlegend=False,
)
fig_bar.update_yaxes(gridcolor="#e5e7eb")

fig_pie = px.pie(
		df_reg,
		names="regiao",
		values="area_ha",
		color="regiao",
		color_discrete_map=colors,
		hole=0.52,
)
fig_pie.update_traces(
		textposition="inside",
		texttemplate="%{label}<br>%{percent}",
		hovertemplate="<b>%{label}</b><br>Área: %{value:,.2f} ha<br>Participação: %{percent}<extra></extra>",
)
fig_pie.update_layout(
		title="🧭 Participação relativa das regiões",
		paper_bgcolor="white",
		margin=dict(l=20, r=20, t=56, b=20),
		legend_title_text="Região",
)

fig_rank = px.bar(
		df_uf.sort_values("area_ha", ascending=True),
		x="area_ha",
		y="UF",
		orientation="h",
		color="regiao",
		color_discrete_map=colors,
		text="area_label",
)
fig_rank.update_traces(
		hovertemplate="<b>%{y}</b><br>Região: %{customdata[0]}<br>Área: %{x:,.2f} ha<extra></extra>",
		customdata=df_uf.sort_values("area_ha", ascending=True)[["regiao"]].values,
		textposition="outside",
)
fig_rank.update_layout(
		title="🏆 Ranking das UFs por área de manguezais",
		paper_bgcolor="white",
		plot_bgcolor="white",
		margin=dict(l=20, r=40, t=56, b=20),
		xaxis_title="Área (ha)",
		yaxis_title="",
		legend_title_text="Região",
)
fig_rank.update_xaxes(gridcolor="#e5e7eb")

fig_tree = px.treemap(
		df_uf,
		path=[px.Constant("Brasil"), "regiao", "UF"],
		values="area_ha",
		color="regiao",
		color_discrete_map=colors,
)
fig_tree.update_traces(
		hovertemplate="<b>%{label}</b><br>Área: %{value:,.2f} ha<extra></extra>",
		textinfo="label+value",
)
fig_tree.update_layout(
		title="🗂️ Hierarquia espacial: Brasil → Região → UF",
		paper_bgcolor="white",
		margin=dict(l=20, r=20, t=56, b=20),
)

summary_rows = []
for _, row in reg_summary.iterrows():
		color = colors[row["regiao"]]
		summary_rows.append(
				f"""
				<tr>
					<td><span class="dot" style="background:{color};"></span>{row['regiao']}</td>
					<td>{int(row['ufs'])}</td>
					<td>{format_ha(row['area_total'])} ha</td>
					<td>{row['percentual']:.1f}%</td>
					<td>{format_ha(row['media_uf'])} ha</td>
					<td>{row['maior_uf']}</td>
				</tr>
				"""
		)
summary_table = "\n".join(summary_rows)

uf_rows = []
for _, row in df_uf.sort_values("area_ha", ascending=False).iterrows():
		color = colors[row["regiao"]]
		uf_rows.append(
				f"""
				<tr>
					<td>{row['UF']}</td>
					<td><span class="dot" style="background:{color};"></span>{row['regiao']}</td>
					<td>{format_ha(row['area_ha'])} ha</td>
					<td>{row['percentual_nacional']:.2f}%</td>
				</tr>
				"""
		)
uf_table = "\n".join(uf_rows)

insights = [
		f"A região <b>{maior_regiao['regiao']}</b> concentra <b>{maior_regiao['percentual']:.1f}%</b> da área nacional de manguezais.",
		f"A UF com maior extensão é <b>{maior_uf['UF']}</b>, com <b>{format_ha(maior_uf['area_ha'])} ha</b>.",
		f"As regiões <b>Norte</b> e <b>Nordeste</b> somam <b>{(df_reg[df_reg['regiao'].isin(['Norte', 'Nordeste'])]['area_ha'].sum() / total_area * 100):.1f}%</b> do total nacional.",
		f"O conjunto analisado reúne <b>{format_int(total_ufs)}</b> unidades federativas distribuídas em <b>{format_int(total_regioes)}</b> macrorregiões brasileiras.",
]
insights_html = "".join(f"<li>{item}</li>" for item in insights)

cards_html = f"""
<section class="stats-grid">
	<div class="stat-card accent-a">
		<div class="stat-label">🌿 Área total de manguezais</div>
		<div class="stat-value">{format_ha(total_area)} ha</div>
		<div class="stat-note">Soma das áreas regionais consolidadas</div>
	</div>
	<div class="stat-card accent-b">
		<div class="stat-label">🧭 Região líder</div>
		<div class="stat-value">{maior_regiao['regiao']}</div>
		<div class="stat-note">{format_ha(maior_regiao['area_ha'])} ha</div>
	</div>
	<div class="stat-card accent-c">
		<div class="stat-label">📍 UFs com ocorrência</div>
		<div class="stat-value">{format_int(total_ufs)}</div>
		<div class="stat-note">Manguezais registrados na base oficial</div>
	</div>
	<div class="stat-card accent-d">
		<div class="stat-label">📈 Média por região</div>
		<div class="stat-value">{format_ha(media_regional)} ha</div>
		<div class="stat-note">Área média entre as quatro regiões</div>
	</div>
</section>
"""

about_html = """
<section class="panel about-panel">
	<h2>📋 Sobre esta análise</h2>
	<p>
		Este dashboard apresenta a distribuição geográfica dos manguezais brasileiros a partir de uma base
		consolidada por unidade federativa e macrorregião. O objetivo é apoiar sínteses visuais, comparações
		regionais e comunicação pública em ambiente web.
	</p>
	<ul>
		<li><b>Fonte dos dados:</b> ICMBio / IBGE</li>
		<li><b>Autor:</b> Ronan Caetano</li>
		<li><b>Ano:</b> 2026</li>
		<li><b>Projeção de referência do projeto:</b> SIRGAS 2000 (EPSG 4674)</li>
	</ul>
	<div class="action-links">
		<a href="mapa_manguezais_por_uf_cor_regiao.html" target="_blank">🗺️ Ver mapa interativo</a>
		<a href="../index.html" target="_blank">🏠 Página inicial do projeto</a>
	</div>
</section>
"""

dashboard_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Dashboard dos Manguezais Brasileiros</title>
	<style>
		:root {{
			--bg: #eef4fb;
			--panel: #ffffff;
			--text: #0f172a;
			--muted: #64748b;
			--line: #dbe4ef;
			--shadow: 0 14px 36px rgba(15, 23, 42, 0.10);
			--radius: 20px;
		}}
		* {{ box-sizing: border-box; }}
		body {{
			margin: 0;
			font-family: "Segoe UI", Arial, sans-serif;
			background:
				radial-gradient(circle at top left, rgba(29, 78, 216, 0.18), transparent 22%),
				linear-gradient(180deg, #f6fbff 0%, var(--bg) 100%);
			color: var(--text);
		}}
		.container {{ max-width: 1380px; margin: 0 auto; padding: 26px; }}
		.hero {{
			background: linear-gradient(135deg, #0f766e 0%, #1d4ed8 52%, #4338ca 100%);
			color: #fff;
			border-radius: 24px;
			padding: 28px 30px;
			box-shadow: var(--shadow);
			margin-bottom: 20px;
			position: relative;
			overflow: hidden;
		}}
		.hero::after {{
			content: "";
			position: absolute;
			inset: auto -80px -80px auto;
			width: 240px;
			height: 240px;
			background: rgba(255,255,255,0.08);
			border-radius: 50%;
		}}
		.hero h1 {{ margin: 0 0 8px; font-size: 34px; line-height: 1.1; }}
		.hero p {{ margin: 0; max-width: 880px; font-size: 15px; line-height: 1.6; opacity: 0.96; }}
		.hero-meta {{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 16px; }}
		.meta-pill {{
			background: rgba(255,255,255,0.14);
			border: 1px solid rgba(255,255,255,0.18);
			border-radius: 999px;
			padding: 8px 12px;
			font-size: 12px;
		}}
		.stats-grid {{
			display:grid;
			grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
			gap: 16px;
			margin-bottom: 20px;
		}}
		.stat-card, .panel {{
			background: var(--panel);
			border-radius: var(--radius);
			box-shadow: var(--shadow);
			padding: 20px;
		}}
		.stat-card {{ position: relative; overflow:hidden; }}
		.stat-card::before {{
			content: "";
			position:absolute;
			top:0; left:0; right:0;
			height: 6px;
		}}
		.accent-a::before {{ background:#0f766e; }}
		.accent-b::before {{ background:#e31a1c; }}
		.accent-c::before {{ background:#1d4ed8; }}
		.accent-d::before {{ background:#6a3d9a; }}
		.stat-label {{ color: var(--muted); font-size: 13px; margin-bottom: 10px; }}
		.stat-value {{ font-size: 29px; font-weight: 700; line-height: 1.15; }}
		.stat-note {{ margin-top: 8px; color: var(--muted); font-size: 12px; }}
		.panel h2 {{ margin:0 0 8px; font-size: 24px; }}
		.panel p {{ margin:0; line-height: 1.6; color: #334155; }}
		.top-grid {{
			display:grid;
			grid-template-columns: 1.15fr 0.85fr;
			gap: 20px;
			margin-bottom: 20px;
		}}
		.chart-grid {{
			display:grid;
			grid-template-columns: 1fr 1fr;
			gap: 20px;
			margin-bottom: 20px;
		}}
		.bottom-grid {{
			display:grid;
			grid-template-columns: 0.95fr 1.05fr;
			gap: 20px;
			margin-bottom: 20px;
		}}
		.plot-wrap {{ min-height: 420px; }}
		.plot-wrap .plotly-graph-div {{ width:100% !important; }}
		.summary-table, .uf-table {{ width:100%; border-collapse: collapse; font-size: 14px; }}
		.summary-table th, .summary-table td, .uf-table th, .uf-table td {{
			padding: 10px 8px;
			border-bottom: 1px solid var(--line);
			text-align:left;
		}}
		.summary-table th, .uf-table th {{
			color: var(--muted);
			text-transform: uppercase;
			font-size: 12px;
			letter-spacing: 0.04em;
		}}
		.dot {{ width:12px; height:12px; border-radius:50%; display:inline-block; margin-right:8px; vertical-align:middle; }}
		.insights {{ margin: 0; padding-left: 18px; line-height: 1.8; color:#334155; }}
		.action-links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top: 18px; }}
		.action-links a {{
			text-decoration:none;
			color:#0f172a;
			background:#f8fafc;
			border:1px solid var(--line);
			padding:10px 14px;
			border-radius:12px;
			font-weight:600;
		}}
		.footer {{ text-align:center; color: var(--muted); font-size: 12px; padding: 6px 0 18px; }}
		@media (max-width: 1080px) {{
			.top-grid, .chart-grid, .bottom-grid {{ grid-template-columns: 1fr; }}
		}}
	</style>
</head>
<body>
	<div class="container">
		<section class="hero">
			<h1>🌿 Distribuição Geográfica dos Manguezais Brasileiros</h1>
			<p>
				Dashboard interativo inspirado no modelo de apresentação pública do portfólio, com indicadores,
				gráficos dinâmicos, ranking territorial e síntese analítica por macrorregião brasileira.
			</p>
			<div class="hero-meta">
				<span class="meta-pill">📍 {format_int(total_ufs)} UFs com ocorrência</span>
				<span class="meta-pill">🧭 {format_int(total_regioes)} regiões com manguezais</span>
				<span class="meta-pill">🌱 {format_ha(total_area)} ha mapeados</span>
				<span class="meta-pill">📅 Ano 2026</span>
			</div>
		</section>

		{cards_html}

		<section class="top-grid">
			{about_html}
			<section class="panel">
				<h2>💡 Principais insights</h2>
				<ul class="insights">
					{insights_html}
				</ul>
			</section>
		</section>

		<section class="chart-grid">
			<section class="panel plot-wrap">
				{fig_html(fig_bar, include_js=True)}
			</section>
			<section class="panel plot-wrap">
				{fig_html(fig_pie)}
			</section>
		</section>

		<section class="chart-grid">
			<section class="panel plot-wrap">
				{fig_html(fig_rank)}
			</section>
			<section class="panel plot-wrap">
				{fig_html(fig_tree)}
			</section>
		</section>

		<section class="bottom-grid">
			<section class="panel">
				<h2>📊 Síntese regional</h2>
				<p style="margin-bottom: 14px; color:#64748b;">Comparação entre número de UFs, área total, participação relativa e maior unidade federativa por região.</p>
				<table class="summary-table">
					<thead>
						<tr>
							<th>Região</th>
							<th>UFs</th>
							<th>Área total</th>
							<th>% Brasil</th>
							<th>Média por UF</th>
							<th>Maior UF</th>
						</tr>
					</thead>
					<tbody>
						{summary_table}
					</tbody>
				</table>
			</section>

			<section class="panel">
				<h2>📍 Detalhamento por UF</h2>
				<p style="margin-bottom: 14px; color:#64748b;">Tabela ordenada da maior para a menor área de manguezais no conjunto nacional.</p>
				<div style="max-height: 520px; overflow:auto;">
					<table class="uf-table">
						<thead>
							<tr>
								<th>UF</th>
								<th>Região</th>
								<th>Área</th>
								<th>% Brasil</th>
							</tr>
						</thead>
						<tbody>
							{uf_table}
						</tbody>
					</table>
				</div>
			</section>
		</section>

		<div class="footer">
			Desenvolvido com Python e Plotly para publicação estática em GitHub Pages · Fonte: ICMBio / IBGE · Autor: Ronan Caetano
		</div>
	</div>
</body>
</html>
"""

out = out_dir / "dashboard_manguezais_regioes.html"
out.write_text(dashboard_html, encoding="utf-8")

print("Dashboard", out)
