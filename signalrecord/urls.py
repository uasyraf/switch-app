from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cleandata/", views.cleandata, name="cleandata"),
    path("rawdata/", views.rawdata, name="rawdata"),
    path("reports/", views.reports, name="reports"),
]