from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# Create your views here.
from .models import Post
from .forms import PostForm

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form":form,
    }
    return render(request, "post_form.html", context)

def post_detail(request,id):
    instance = get_object_or_404(Post, id=id)
    context ={
    "title": instance.title,
    "instance":instance,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    # In revese order of timestap then
    queryset_list = Post.objects.all()
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
    "title": "Authenticated list",
    "page_request_var":page_request_var
    }
    return render(request, "post_list.html", context)

def post_update(request, id =None):
    instance = get_object_or_404(Post, id=id)
    # instance=instance is to be added to retrive data to form.
    # Here insted of queryset we used instance which is dict
    form = PostForm(request.POST or None,instance=instance)
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

def post_delete(request, id =None):
    instance = get_object_or_404(Post, id=id)
    # This line will delete that line form database.
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")
