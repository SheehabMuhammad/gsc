from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("properties/", views.properties, name="properties"),
    path("properties/<int:property_id>/", views.property, name="property"),
    path("property/<int:property_id>/urls/", views.property_urls, name="property_urls"),
    path(
        "property/<int:property_id>/scrape",
        views.property_scrape,
        name="property_scrape",
    ),
    path("urls/", views.urls, name="urls"),
    path("urls/<int:url_id>/", views.url, name="url"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
