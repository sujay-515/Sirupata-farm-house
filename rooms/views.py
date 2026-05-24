from django.shortcuts import render

from ml_engine.services.analytics import get_room_popularity_map
from ml_engine.services.recommendations import recommend_similar_items
from core.views import get_site_content
from .catalog import get_public_rooms


def rooms(request):
    popularity = get_room_popularity_map()

    rooms_data = []
    for room in get_public_rooms():
        room_data = room.copy()
        room_data["bookings"] = popularity.get(room["name"], 0)
        rooms_data.append(room_data)

    rooms_data.sort(key=lambda x: x['bookings'], reverse=True)

    seed_name = request.GET.get("seed", rooms_data[0]["name"] if rooms_data else None)
    recommended_rooms = recommend_similar_items(rooms_data, seed_name=seed_name, limit=3)

    return render(request, "rooms/room.html", {
        "rooms": rooms_data,
        "popular_rooms": rooms_data[:3],
        "recommended_rooms": recommended_rooms,
        "site_content": get_site_content(),
    })
