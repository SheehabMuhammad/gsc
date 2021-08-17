from django.contrib import admin
from .models import Property, Url

# class UrlInline(admin.TabularInline):
#     model = Url


class PropertyAdmin(admin.ModelAdmin):
    # inlines = [UrlInline]
    list_display = ("name", "property", "description", "created_at", "updated_at")


class UrlAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "c_type",
        "c_status",
        "crawled_at",
        "mu_type",
        "mu_status",
        "detected_at",
        "created_at",
    )
    list_filter = ("property__property",)
    list_max_show_all = 1000
    list_per_page = 500


admin.site.register(Property, PropertyAdmin)
admin.site.register(Url, UrlAdmin)
