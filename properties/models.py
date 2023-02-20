from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    property = models.URLField(unique=True)
    resource_id = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    options = models.TextField(blank=True)
    priority_coverage = models.CharField(max_length=100, default="low")
    priority_backlink = models.CharField(max_length=100, default="low")
    last_scraped = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property

    class Meta:
        verbose_name_plural = "Properties"


class Url(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.URLField()
    c_type = models.CharField(blank=True, default="Not listed", null=True, max_length=255)
    c_status = models.CharField(blank=True, default="Not listed", null=True, max_length=255)
    crawled_at = models.DateTimeField(default=None, null=True)
    mu_type = models.CharField(default="Not listed", blank=True, null=True, max_length=255)
    mu_status = models.CharField(default="Not listed as mobile friendly", blank=True, null=True, max_length=255)
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


class Filter(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    type = models.CharField(default="Unknown", max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "value", "type"], name="unique filter constraint"
            )
        ]


class Backlink(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    backlink = models.CharField(max_length=512)
    authority = models.IntegerField(default=0, blank=True, null=True)
    crawled_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.backlink

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property", "backlink"], name="unique property backlink constraint"
            )
        ]


class Tag(models.Model):
    name = models.CharField(max_length=255)
    expressions = models.JSONField()
    scope = models.CharField(default="Universal", max_length=255)

    def __str__(self):
        return self.name + " - " + self.scope

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "scope"], name="unique tag constraint"
            )
        ]




class Log(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True, null=True)
    num_urls = models.IntegerField(default=0, null=True)
    time_taken = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    scrape_priority = models.CharField(max_length=100, default="low")
    created_at = models.DateTimeField(auto_now_add=True)
