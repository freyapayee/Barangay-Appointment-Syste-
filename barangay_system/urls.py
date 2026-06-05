from django.contrib import admin
from django.urls import include, path

from appointments.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("residents/", include("residents.urls")),
    path("services/", include("services.urls")),
    path("appointments/", include("appointments.urls")),
]
