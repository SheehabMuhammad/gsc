from django.contrib import admin
from .models import Property, Url, Backlink, Tag

# class UrlInline(admin.TabularInline):
#     model = Url


class PropertyAdmin(admin.ModelAdmin):
    # inlines = [UrlInline]
    list_display = ("property", "description", "created_at", "updated_at")


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

class BacklinkAdmin(admin.ModelAdmin):
    list_display = (
        "backlink",
        "authority",
        "crawled_at",
        "created_at",
        "updated_at"
    )
    list_filter = ("property__property",)
    list_max_show_all = 1000
    list_per_page = 500

class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "expressions",
        "scope"
    )
    list_max_show_all = 1000
    list_per_page = 100

admin.site.register(Property, PropertyAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(Backlink, BacklinkAdmin)
admin.site.register(Tag, TagAdmin)
