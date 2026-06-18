from typing import List, Dict, Tuple, Any, Optional


def render_itinerary_map(
    destination_coords: Tuple[float, float],
    day_activities: List[Dict[str, Any]],
    zoom: int = 10,
) -> str:
    try:
        import folium
    except ImportError:
        return _render_fallback_map(destination_coords, zoom)

    lat, lng = destination_coords
    m = folium.Map(location=[lat, lng], zoom_start=zoom, tiles="OpenStreetMap")

    colors = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen"]
    for day_data in day_activities:
        day = day_data.get("day", 1)
        color = colors[(day - 1) % len(colors)]
        locs = day_data.get("locations", [])
        coords_list = []
        for loc in locs:
            name, mlat, mlng = loc[0], loc[1], loc[2]
            folium.Marker(
                location=[mlat, mlng],
                popup=f"Day {day}: {name}",
                icon=folium.Icon(color=color, icon="info-sign"),
            ).add_to(m)
            coords_list.append([mlat, mlng])
        if len(coords_list) >= 2:
            folium.PolyLine(coords_list, color=color, weight=3, popup=f"Day {day} route").add_to(m)

    return m._repr_html_()


def _render_fallback_map(destination_coords: Tuple[float, float], zoom: int = 10) -> str:
    lat, lng = destination_coords
    return (
        f'<iframe src="https://www.google.com/maps?q={lat},{lng}&z={zoom}&output=embed" '
        f'width="100%" height="500" style="border:0;" allowfullscreen loading="lazy"></iframe>'
    )
