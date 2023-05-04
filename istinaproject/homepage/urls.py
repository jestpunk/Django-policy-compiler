from django.urls import path

from . import views

urlpatterns = [
    path("", views.startpage_view, name="startpage_view"),
]