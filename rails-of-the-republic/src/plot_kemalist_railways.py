import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

# Load data
railways = gpd.read_file("data/synthetic_railways.geojson")
regions = gpd.read_file("data/synthetic_regions.geojson")

quotes = [
    {"location": "Ankara-Sivas", "text": "Demiryolu, Türk köylüsünü esaretten kurtaracaktır."},
    {"location": "Kayseri-Sivas", "text": "Demiryolu yapımı millî ülkü haline gelmelidir."}
]

fig, ax = plt.subplots(figsize=(10,8))
colors = {"Halkçılık": "green", "Devletçilik": "blue", "Yabancı sermaye": "red"}

for idx, row in railways.iterrows():
    ax.plot(*row.geometry.xy, color=colors[row.ideology_tag], linewidth=3, label=row.ideology_tag)

regions.plot(ax=ax, color='orange', markersize=(regions['literacy_1938'] - regions['literacy_1923'])*10)

for q in quotes:
    line = railways[railways['name'] == q['location']].geometry.values[0]
    mid = line.interpolate(0.5, normalized=True)
    ax.text(mid.x, mid.y, q['text'], fontsize=9, bbox=dict(facecolor='white', alpha=0.6))

ax.set_title('Kemalist Demiryolu Genişlemesi ve İdeolojik Bağlantıları (Örnek Veri)', fontsize=14)
ax.legend(colors.keys())
ax.set_xlabel('Boylam')
ax.set_ylabel('Enlem')
plt.show()
