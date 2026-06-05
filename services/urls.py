from django.urls import path

from . import views


urlpatterns = [
    path("", views.ApplicationListView.as_view(), name="application_list"),
    path("add/", views.ApplicationCreateView.as_view(), name="application_add"),
    path("<int:pk>/", views.ApplicationDetailView.as_view(), name="application_detail"),
    path("<int:pk>/edit/", views.ApplicationUpdateView.as_view(), name="application_edit"),
    path("<int:pk>/delete/", views.ApplicationDeleteView.as_view(), name="application_delete"),
]
