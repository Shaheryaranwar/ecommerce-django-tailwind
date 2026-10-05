from django.urls import path

from . import views

app_name = "community"

urlpatterns = [
    path("", views.showcase, name="showcase"),
    path("project/<int:pk>/", views.project_detail, name="project_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("project/add/", views.project_add, name="project_add"),
    path("project/<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("project/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("image/<int:pk>/delete/", views.image_delete, name="image_delete"),
]
