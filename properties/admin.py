from django.contrib import admin
from .models import Property, Url


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'description', 'created_at', 'updated_at')


class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'c_type', 'c_status', 'crawled_at', 'mu_type', 'mu_status', 'detected_at', 'created_at')


admin.site.register(Property, PropertyAdmin)
admin.site.register(Url, UrlAdmin)
