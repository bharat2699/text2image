from django.urls import path
from . import views

urlpatterns = [
    path("", views.TtiViews.as_view(), name="tti_views"),
]
