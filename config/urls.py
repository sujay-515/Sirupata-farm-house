from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from config.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),

    # App routes
    path('', include('core.urls')),
    
    path('rooms/', include('rooms.urls')),
    path('gallery/', include('gallery.urls')),
    path('bookings/', include('bookings.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
