from django.urls import path

from . import views


urlpatterns = [
    path("", views.resident_list, name="resident_list"),
    path("add/", views.resident_add, name="resident_add"),
    path("<int:pk>/", views.resident_detail, name="resident_detail"),
    path("<int:pk>/edit/", views.resident_edit, name="resident_edit"),
    path("<int:pk>/delete/", views.resident_delete, name="resident_delete"),
]
