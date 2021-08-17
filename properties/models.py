from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    name = models.CharField(max_length=100)
    property = models.URLField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    options = models.TextField(blank=True)
    crawl_priority = models.CharField(max_length=100, default="low")
    last_crawled = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Properties"


class Url(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.URLField()
    c_type = models.CharField(blank=True, null=True, max_length=255)
    c_status = models.CharField(blank=True, null=True, max_length=255)
    crawled_at = models.DateTimeField(default=None, null=True)
    mu_type = models.CharField(blank=True, null=True, max_length=255)
    mu_status = models.CharField(
        default="Not listed as mobile friendly", blank=True, null=True, max_length=255
    )
    detected_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property", "url"], name="unique property url constraint"
            )
        ]


class Option(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Options"
