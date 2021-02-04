from django.contrib import admin
from django.urls import path, include

from dashboard import urls as dashboard_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(dashboard_urls)),
]
