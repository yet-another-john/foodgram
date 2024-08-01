# isort: skip_file
"""Main urls."""

from django.contrib import admin
from django.urls import include, path

from api.views import redirection  # isort: skip


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('s/<str:short_url>/', redirection),
]
