from django.db.utils import OperationalError, ProgrammingError

from .models import Room


LEGACY_ROOM_CONTENT = {
    "Deluxe Room": {
        "image": "core/sections/hill1.jpg",
        "capacity": "1-2 guests",
        "amenities": ["King Bed", "Free Wi-Fi", "Breakfast", "Mountain View"],
        "sort_order": 1,
    },
    "Luxury Suite": {
        "image": "core/sections/hill3.jpg",
        "capacity": "2-4 guests",
        "amenities": ["Living Area", "Free Wi-Fi", "Bathtub", "Panoramic View", "Mini Bar"],
        "sort_order": 2,
    },
    "Farmhouse Suite": {
        "image": "core/sections/farm1.jpg",
        "capacity": "2-4 guests",
        "amenities": ["Garden View", "Private Balcony", "Free Wi-Fi", "Breakfast"],
        "sort_order": 3,
    },
}


def _normalize_amenities(raw_value, fallback):
    if not raw_value:
        return fallback
    text = str(raw_value).replace("\r", "\n")
    parts = text.split("\n") if "\n" in text else text.split(",")
    cleaned = [item.strip() for item in parts if item.strip()]
    return cleaned or fallback


def get_public_rooms():
    try:
        raw_rooms = list(
            Room.objects.filter(is_available=True)
            .values("name", "price", "description", "image_file", "image", "capacity", "amenities", "sort_order")
        )
    except (OperationalError, ProgrammingError):
        raw_rooms = list(
            Room.objects.filter(is_available=True)
            .values("name", "price", "description")
        )

    rooms = []
    for room in raw_rooms:
        fallback = LEGACY_ROOM_CONTENT.get(room["name"], {})
        rooms.append(
            {
                "name": room["name"],
                "price": room["price"],
                "description": room["description"],
                "image_file": room.get("image_file", ""),
                "image": room.get("image") or fallback.get("image", "core/sections/farm1.jpg"),
                "capacity": room.get("capacity") or fallback.get("capacity", ""),
                "amenity_list": _normalize_amenities(room.get("amenities"), fallback.get("amenities", [])),
                "sort_order": room.get("sort_order", fallback.get("sort_order", 999)),
            }
        )

    rooms.sort(key=lambda item: (item["sort_order"], item["name"]))
    return rooms
