from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("library/<str:library_id>/", views.library, name="library"),
]
