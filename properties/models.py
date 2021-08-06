from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    name = models.CharField(max_length=100)
    domain = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    coverage_url = models.URLField(blank=True)
    musability_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    options = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Properties"


class Url(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.URLField(unique=True)
    c_type = models.CharField(blank=True, null=True, max_length=255)
    c_status = models.CharField(blank=True, null=True, max_length=255)
    crawled_at = models.DateTimeField(default=None, null=True)
    mu_type = models.CharField(blank=True, null=True, max_length=255)
    mu_status = models.CharField(blank=True, null=True, max_length=255)
    detected_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


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


