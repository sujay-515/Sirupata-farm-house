from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # App routes
    path('', include('core.urls')),
    
    path('rooms/', include('rooms.urls')),
    path('gallery/', include('gallery.urls')),
    path('bookings/', include('bookings.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
