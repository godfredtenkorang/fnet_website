from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('tlgh/admin/', admin.site.urls),
    path('', include('my_site.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('rental/', include('rental.urls')),
    path('account/', include('users.urls')),
    path('', include('flight.urls')),
    path('', include('rent.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'my_site.views.custom_404_view'