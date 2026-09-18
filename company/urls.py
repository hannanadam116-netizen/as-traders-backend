from django.urls import path

from .views import (
    CompanyView,
    CompanyDetailView,
)

urlpatterns = [

    path(
        "",
        CompanyView.as_view(),
        name="company",
    ),

    path(
        "details/",
        CompanyDetailView.as_view(),
        name="company-details",
    ),

]