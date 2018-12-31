from urllib.parse import quote
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from .models import Post
from .forms import PostForm

def post_create(request):
    # This line is updated
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # Add this below code if the above verification is not there
    # if not request.user.is_authenticated():
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # This assumed that the user is logged in bez Http404 checks it
        # This is newly added line
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form":form,
    }
    return render(request, "post_form.html", context)

def post_detail(request,slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    # The content share string is passed here
    share_string= quote(instance.content)
    # and it is passed into the context
    context ={
    "title": instance.title,
    "instance":instance,
    "share_string":share_string,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    # the below two line segments are added now
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
        Q(title__icontains = query) |
        Q(content__icontains = query) |
        Q(user__first_name__icontains = query) |
        Q(user__last_name__icontains = query)
        ).distinct()

    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page_request_var = "abc"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context ={
    "object_list":queryset,
    "title": "List",
    "page_request_var":page_request_var,
    "today":today,
    }
    return render(request, "post_list.html", context)

def post_update(request, slug =None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    # Here it request.FILES or None is added
    form = PostForm(request.POST or None,request.FILES or None ,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #extra_tag="some-tag" added to have addon class.
        messages.success(request, "<a href='#'>Item </a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context ={
    "title": instance.title,
    "instance":instance,
    "form":form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug =None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    # This line will delete that line form database.
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")
