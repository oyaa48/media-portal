from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("library/<str:library_id>/", views.library, name="library"),
    path("seasons/<str:show_id>/", views.seasons, name="seasons"),
    path("item/<str:item_id>/", views.item, name="item"),
    path("subtitle/<str:item_id>/<int:stream_index>/", views.subtitle, name="subtitle"),
    path("report-progress/", views.report_progress, name="report_progress"),
    path("playback-started/", views.playback_started, name="playback_started"),
    path("login/", views.login_view, name="login"),
]
