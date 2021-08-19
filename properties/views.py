from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse

from .models import Property, Url, Log


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
    User = get_user_model()
    users = User.objects.all()
    user_num = users.count()

    logs = Log.objects.all()

    context = {
        "properties": properties,
        "user_num": user_num,
        "users": users,
        "logs": logs,
    }

    return render(request, "overview/index.html", context)


@login_required(login_url="/login/")
def properties(request):

    if request.method == "POST":
        name = request.POST["name"]
        property = request.POST["property"]
        if name and property:
            try:
                property = Property(
                    name=name, property=property, owner_id=request.user.id
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
    property = Property.objects.all()
    return render(request, "properties/index.html", {"property": property})


@login_required(login_url="/login/")
def property_scrape(request, property_id):
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

    property = Property.objects.get(id=property_id)

    properties = Property.objects.all()

    urls = property.url_set.all()

    # Show 25 contacts per page
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

    return render(
        request,
        "urls/index.html",
        {"property": property, "urls": urls, "properties": properties},
    )


@login_required(login_url="/login/")
def urls(request):
    properties = Property.objects.all()

    urls = Url.objects.all()

    # Show 25 contacts per page
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

    return render(request, "urls/index.html", {"urls": urls, "properties": properties})


@login_required(login_url="/login/")
def logs(request):
    logs = Log.objects.all()
    return render(request, "logs/index.html", {"logs": logs})


@login_required(login_url="/login/")
def url(request, url_id):
    url = Url.objects.all()
    return render(request, "url/index.html", {"url": url})
