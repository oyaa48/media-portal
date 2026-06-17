from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("library/<str:library_id>/", views.library, name="library"),
    path("item/<str:item_id>/", views.item, name="item"),
    path("subtitle/<str:item_id>/<int:stream_index>/", views.subtitle, name="subtitle"),
]
