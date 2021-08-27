from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from .models import Property, Url, Log, Filter


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

    some_day_last_week = datetime.now() - timedelta(days=20)

    print("day: ", some_day_last_week)

    urls_by_date = (
        Url.objects.filter(
            created_at__gte=some_day_last_week,
        )
        .annotate(
            day=TruncDay("created_at"),
            created_count=Count("created_at__date"),
        )
        .values(
            "day",
            "created_count",
        )
    )

    logs = Log.objects.all()

    context = {
        "properties": properties,
        "urls_by_date": urls_by_date,
        "logs": logs,
    }

    print(urls_by_date)
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
                    property=property, resource_id=resource_id, owner_id=request.user.id
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
    messages.info(
        request,
        "Property tranferred to high priority scraper, scraping will be completed in next minutes.",
    )
    return redirect(reverse("properties"))


@login_required(login_url="/login/")
def property_urls(request, property_id):
    timezone.activate(pytz.timezone("America/Chicago"))

    property = Property.objects.get(id=property_id)
    properties = Property.objects.all()
    urls = property.url_set.all()
    filters = Filter.objects.all()

    c_type = request.GET.getlist("c_type[]")
    c_status = request.GET.getlist("c_status[]")
    mu_type = request.GET.getlist("mu_type[]")
    mu_status = request.GET.getlist("mu_status[]")
    search = request.GET.get("search")

    if c_type:
        urls = urls.filter(c_type__in=c_type)
    if c_status:
        urls = urls.filter(c_status__in=c_status)
    if mu_type:
        urls = urls.filter(mu_type__in=mu_type)
    if mu_status:
        urls = urls.filter(mu_status__in=mu_status)
    if search:
        urls = urls.filter(url__icontains=search)

    # Show 1000 urls per page
    paginator = Paginator(urls, 1000)

    page = request.GET.get("page")

    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        urls = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        urls = paginator.page(paginator.num_pages)

    context = {
        "property": property,
        "urls": urls,
        "properties": properties,
        "filters": filters,
        "c_status": c_status,
        "c_type": c_type,
        "mu_status": mu_status,
        "mu_type": mu_type,
        "search": search,
        "show_selector": True,
    }

    return render(request, "urls/index.html", context)


@login_required(login_url="/login/")
def urls(request):
    timezone.activate(pytz.timezone("America/Chicago"))

    properties = Property.objects.all()
    urls = Url.objects.all()

    filters = Filter.objects.all()

    c_type = request.GET.getlist("c_type[]")
    c_status = request.GET.getlist("c_status[]")
    mu_type = request.GET.getlist("mu_type[]")
    mu_status = request.GET.getlist("mu_status[]")
    search = request.GET.get("search")

    if c_type:
        urls = urls.filter(c_type__in=c_type)
    if c_status:
        urls = urls.filter(c_status__in=c_status)
    if mu_type:
        urls = urls.filter(mu_type__in=mu_type)
    if mu_status:
        urls = urls.filter(mu_status__in=mu_status)
    if search:
        urls = urls.filter(url__icontains=search)

    # Show 1000 urls per page
    paginator = Paginator(urls, 1000)

    page = request.GET.get("page")

    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        urls = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        urls = paginator.page(paginator.num_pages)

    context = {
        "properties": properties,
        "urls": urls,
        "filters": filters,
        "c_status": c_status,
        "c_type": c_type,
        "mu_status": mu_status,
        "mu_type": mu_type,
        "search": search,
        "show_selector": True,
    }

    return render(request, "urls/index.html", context)


@login_required(login_url="/login/")
def logs(request):
    timezone.activate(pytz.timezone("America/Chicago"))
    logs = Log.objects.all()
    return render(request, "logs/index.html", {"logs": logs})


@login_required(login_url="/login/")
def url(request, url_id):
    timezone.activate(pytz.timezone("America/Chicago"))
    url = Url.objects.all()
    return render(request, "url/index.html", {"url": url})


def sync_filters(request):
    c_status = Url.objects.order_by().values_list("c_status", flat=True).distinct()
    for status in c_status:
        try:
            filter = Filter.objects.get(name="c_status", value=status)
        except ObjectDoesNotExist:
            filter = Filter(name="c_status", value=status)
            filter.save()

    c_type = Url.objects.order_by().values_list("c_type", flat=True).distinct()
    for status in c_type:
        try:
            filter = Filter.objects.get(name="c_type", value=status)
        except ObjectDoesNotExist:
            filter = Filter(name="c_type", value=status)
            filter.save()

    mu_status = Url.objects.order_by().values_list("mu_status", flat=True).distinct()
    for status in mu_status:
        try:
            filter = Filter.objects.get(name="mu_status", value=status)
        except ObjectDoesNotExist:
            filter = Filter(name="mu_status", value=status)
            filter.save()

    mu_type = Url.objects.order_by().values_list("mu_type", flat=True).distinct()
    for status in mu_type:
        try:
            filter = Filter.objects.get(name="mu_type", value=status)
        except ObjectDoesNotExist:
            filter = Filter(name="mu_type", value=status)
            filter.save()
