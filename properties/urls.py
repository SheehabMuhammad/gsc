from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("properties/", views.properties, name="properties"),
    path("properties/<int:property_id>/", views.property, name="property"),
    path("property/<int:property_id>/scrape/<str:type>", views.property_scrape, name="property_scrape"),
    path("property/<int:property_id>/urls/", views.property_urls, name="property_urls"),
    path("property/<int:property_id>/backlinks/", views.property_backlinks, name="property_links"),

    path("tag/create", views.create_tag, name="create_tag"),
    path("tags/", views.tags, name="tags"),
    path("tag/update", views.update_tag, name="update_tag"),
    path("tag/<int:tag_id>/delete", views.delete_tag, name="delete_tag"),
    path("tags/add-expression", views.add_expression_to_tag, name="add_expression_to_tag"),

    path("logs", views.logs, name="logs"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]