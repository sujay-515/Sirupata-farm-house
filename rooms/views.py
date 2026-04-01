from django.shortcuts import render
from django.db.models import Count
from core.models import Booking
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOM_AMENITIES_TEXT = {
    "Deluxe Room": "King Bed Free Wi-Fi Breakfast View",
    "Family Room": "4 Guests Free Wi-Fi Smart TV Breakfast",
    "Suite Room": "Living Area Free Wi-Fi Bathtub Panoramic View",
    "Farmhouse Suite": "Garden View Private Balcony Free Wi-Fi Breakfast",
}

ROOMS_BASE = [
    {
        "name": "Deluxe Room",
        "price": "NPR 4,500 / night",
        "image": "core/rooms/deluxe.jpg",
        "amenities": ["King Bed", "Free Wi-Fi", "Breakfast", "View"],
        "description": ROOM_AMENITIES_TEXT["Deluxe Room"],
    },
    {
        "name": "Family Room",
        "price": "NPR 6,500 / night",
        "image": "core/rooms/family.jpg",
        "amenities": ["4 Guests", "Free Wi-Fi", "Smart TV", "Breakfast"],
        "description": ROOM_AMENITIES_TEXT["Family Room"],
    },
    {
        "name": "Suite Room",
        "price": "NPR 9,000 / night",
        "image": "core/rooms/suite.jpg",
        "amenities": ["Living Area", "Free Wi-Fi", "Bathtub", "Panoramic View"],
        "description": ROOM_AMENITIES_TEXT["Suite Room"],
    },
    {
        "name": "Farmhouse Suite",
        "price": "NPR 7,500 / night",
        "image": "core/rooms/farmhouse-suite.jpg",
        "amenities": ["Garden View", "Private Balcony", "Free Wi-Fi", "Breakfast"],
        "description": ROOM_AMENITIES_TEXT["Farmhouse Suite"],
    },
]


def rooms(request):
    # Apply booking-popularity counts
    counts = Booking.objects.values('room').annotate(count=Count('id'))
    popularity = {item['room']: item['count'] for item in counts}

    # Merge base room data with booking counts
    rooms_data = []
    for r in ROOMS_BASE:
        room = r.copy()
        room['bookings'] = popularity.get(r['name'], 0)
        rooms_data.append(room)

    rooms_data.sort(key=lambda x: x['bookings'], reverse=True)

    # Content-based recommendation using room descriptions
    descriptions = [r['description'] for r in rooms_data]
    recommended_rooms = []
    try:
        if len(descriptions) > 1:
            tfidf = TfidfVectorizer().fit_transform(descriptions)
            matrix = cosine_similarity(tfidf)

            # Seed room by fallback to most popular
            seed_name = request.GET.get('seed', rooms_data[0]['name'] if rooms_data else None)
            seed_idx = next((idx for idx, r in enumerate(rooms_data) if r['name'] == seed_name), 0)

            sim_scores = [(idx, score) for idx, score in enumerate(matrix[seed_idx]) if idx != seed_idx]
            sim_scores.sort(key=lambda x: x[1], reverse=True)

            for idx, _ in sim_scores[:3]:
                recommended_rooms.append(rooms_data[idx])
    except Exception as e:
        # Log error and fallback to no recommendations
        print(f"Error in room recommendations: {e}")
        recommended_rooms = []

    return render(request, "rooms/room.html", {
        "rooms": rooms_data,
        "popular_rooms": rooms_data[:3],
        "recommended_rooms": recommended_rooms,
    })
