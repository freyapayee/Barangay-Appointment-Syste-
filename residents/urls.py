from django.urls import path

from . import views


urlpatterns = [
    path("", views.ResidentListView.as_view(), name="resident_list"),
    path("add/", views.ResidentCreateView.as_view(), name="resident_add"),
    path("<int:pk>/", views.ResidentDetailView.as_view(), name="resident_detail"),
    path("<int:pk>/edit/", views.ResidentUpdateView.as_view(), name="resident_edit"),
    path("<int:pk>/delete/", views.ResidentDeleteView.as_view(), name="resident_delete"),
]
