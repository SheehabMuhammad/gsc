from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count
from django.utils import timezone
import pytz
from django.http import JsonResponse
import json

from .models import Property, Url, Log, Filter, Backlink, Tag 


def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Syncing Url filters
                sync_filters(request)
                return redirect(reverse("index"))
            else:
                messages.error(request, "Your account is disabled.")
        else:
            messages.error(request, "Invalid login details supplied.")

    return render(request, "auth/login.html", {})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
def index(request):

    properties = Property.objects.all()
    logs = Log.objects.all().order_by("-id")[:10]

    urls_by_date = (
        Url.objects.extra({"day": "date(created_at)"})
        .values("day")
        .annotate(created_count=Count("id"))
    )

    context = {
        "properties": properties,
        "urls_by_date": urls_by_date,
        "logs": logs,
    }

    return render(request, "overview/index.html", context)


@login_required(login_url="/login/")
def properties(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    if request.method == "POST":

        property = request.POST["property"]
        type = request.POST["type"]

        if type and property:
            if type == "domain":
                resource_id = "sc-domain:" + property
            else:
                resource_id = property
            try:
                property = Property(
                    property=property,
                    resource_id=resource_id,
                    owner_id=request.user.id,
                    scrape_priority="high",
                )
                property.save()
                messages.success(request, "Property registred.")
            except Exception as e:
                messages.error(request, "Property already exists.")
        else:
            messages.error(request, "Property could not be registered.")

    properties = Property.objects.all()
    return render(request, "properties/index.html", {"properties": properties})


@login_required(login_url="/login/")
def property(request, property_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    property = Property.objects.all()
    return render(request, "properties/index.html", {"property": property})


@login_required(login_url="/login/")
def property_scrape(request, property_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    property = Property.objects.get(pk=property_id)
    property.scrape_priority = "high"
    property.save()
    messages.info(request,"Property tranferred to high priority scraper, scraping will be completed in the next few minutes. Priority will reset after URLs are scraped from GSC.",)
    return redirect(reverse("properties"))


@login_required(login_url="/login/")
def property_urls(request, property_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    property = Property.objects.get(id=property_id)

    request.session["property_id"] = property.id
    request.session["property"] = property.property

    properties = Property.objects.all()

    urls = property.url_set.all().order_by("id")
    filters = Filter.objects.all().order_by("-type")

    urls_json = list(urls.values())
    filters_json = list(filters.values())

    context = {
        "property" : property,
        "urls_json": urls_json,
        "filters_json": filters_json,
        "properties": properties,
        "filters": filters,
    }

    return render(request, "urls/index.html", context)


@login_required(login_url="/login/")
def property_backlinks(request, property_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    property = Property.objects.get(id=property_id)

    request.session["property_id"] = property.id
    request.session["property"] = property.property

    properties = Property.objects.all()

    urls = property.backlink_set.all().order_by("id")
    tags = Tag.objects.filter(Q(scope='universal') | Q(scope=property.property))

    backlinks_json = list(urls.values())
    tags_json = list(tags.values())

    context = {
        "properties": properties,
        "property" : property,
        "property_json" : {"id": property.id, "property": property.property},
        "backlinks_json": backlinks_json,
        "tags_json": tags_json,
    }

    return render(request, "backlinks/index.html", context)


@login_required(login_url="/login/")
def tags(request):
    timezone.activate(pytz.timezone("America/Chicago"))

    tags = Tag.objects.all()
    tags_json = list(tags.values())
    return render(request, "tags/index.html", {"tags": tags, "tags_json": tags_json,})


@login_required(login_url="/login/")
def create_tag(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    
    if request.method == "POST":
        data = json.loads(request.body)

        name = data['name']
        expressions = data['expressions']
        scope = data['scope']
        property = data['property']

        if name and expressions and scope:
            try:
                tag = Tag(
                    name=name,
                    expressions=expressions,
                    scope=scope,
                )
                tag.save()
                tags = Tag.objects.filter(Q(scope='universal') | Q(scope=property))
                return JsonResponse({ "tags": list(tags.values()) }, status=200)

            except Exception as e:
                response = "Could not add the tag, error: "+str(e)
        else:
            response = "Tag could not be added, check if all fields are satisfied."
        
        return JsonResponse({"msg":response}, status=201)


@login_required(login_url="/login/")
def update_tag(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    if request.method == "POST":
        data = json.loads(request.body)
        expressions = data['expressions']

        if expressions:
            try:
                tag = Tag.objects.get(pk=data['id'])
                tag.expressions = unique_expressions(expressions)
                tag.save()

                messages.info(request, "Tag updated")

                response = "Tag successfully updated"

            except Exception as e:
                print(e)
                response = "Could not add the tag, error: "+str(e)
        else:
            response = "Tag could not be updated, check if all fields are satisfied."
        
        return JsonResponse({"msg":response}, status=201)


@login_required(login_url="/login/")
def delete_tag(request, tag_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    tag = Tag.objects.get(id=tag_id)
    tag.delete()
    messages.success(request, "Tag deleted.")

    return redirect(tags)

@login_required(login_url="/login/")
def add_expression_to_tag(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    
    if request.method == "POST":
        data = json.loads(request.body)

        expressions = data['expressions']
        tag_id = data['tag_id']
        property = data['property']

        if  expressions and tag_id and property:
            try:
                tag = Tag.objects.get(pk=tag_id)
                tag.expressions = unique_expressions(tag.expressions + expressions)
                tag.save()

                tags = Tag.objects.filter(Q(scope='universal') | Q(scope=property))
                return JsonResponse({ "tags": list(tags.values()) }, status=200)

            except Exception as e:
                response = "Could not add the tag, error: "+str(e)
        else:
            response = "Tag could not be updated, check if all fields are satisfied."

        return JsonResponse({"msg":response}, status=400)

@login_required(login_url="/login/")
def logs(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    logs = Log.objects.all().order_by("-id")
    return render(request, "logs/index.html", {"logs": logs})


def sync_filters(request):
    coverages = Url.objects.order_by().values_list("c_status", "c_type").distinct()
    for coverage in coverages:
        # Create new coverage status filter
        try:
            filter = Filter.objects.get(
                name="c_status", value=coverage[0], type=coverage[0]
            )
        except ObjectDoesNotExist:
            filter = Filter(name="c_status", value=coverage[0], type=coverage[0])
            filter.save()

        try:
            filter = Filter.objects.get(
                name="c_type", value=coverage[1], type=coverage[0]
            )
        except ObjectDoesNotExist:
            filter = Filter(name="c_type", value=coverage[1], type=coverage[0])
            filter.save()

    mus = Url.objects.order_by().values_list("mu_status", "mu_type").distinct()
    for mu in mus:
        # Create new coverage status filter
        try:
            filter = Filter.objects.get(name="mu_status", value=mu[0], type=mu[0])
        except ObjectDoesNotExist:
            filter = Filter(name="mu_status", value=mu[0], type=mu[0])
            filter.save()


def unique_expressions(expressions):
    unique_marker = []
    unique_expressions = []
    for item in expressions:
        if item['expression'] not in unique_marker and bool(item['expression']):
            unique_marker.append(item['expression'])
            unique_expressions.append(item)

    return unique_expressions