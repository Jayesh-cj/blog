from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from .forms import  BlogForm

# Create your views here.

def home(request):
    try:
        blogs = Blog.objects.all()
    except Exception as e:
        print(e)
    return render(request, 'blogs/home.html',{
        'user' : request.user,
        'blogs' : blogs
    })

# Get  blog details
def get_blog(request, id):
    try:
        blog_obj = Blog.objects.get(id = id)
        category = blog_obj.category
        related_blogs = Blog.objects.filter(category = category).exclude(title = blog_obj.title)
    except Exception as e:
        print(e)
    return render(request, 'blogs/blog.html',{
        'blog' : blog_obj,
        'related_blogs' : related_blogs
    })


def create_blog(request):
    if request.user.is_authenticated == False:
        messages.success(request, 'Login required!')
        return redirect('/login')
    
    category = Category.objects.all().order_by("category_name")
    if request.method == 'POST':
        frm = BlogForm(request.POST)
        category = request.POST.get('category')
        title = request.POST.get('title')
        banner = request.FILES.get('banner')

        if frm.is_valid():
            content = frm.cleaned_data['content']

            Blog.objects.create(
                title = title,
                content = content,
                category = Category.objects.get(id = category),
                user = request.user,
                image = banner
            )
            return redirect('/')

    return render(request, 'blogs/create_blog.html',{
        'frm': BlogForm,
        'categories' : category
    })


def edit_blog(request, id):
    try:
        category = Category.objects.all().order_by("category_name")
        blog_obj = Blog.objects.get(id = id)
        if request.method == 'POST':
            frm = BlogForm(request.POST)
            category = request.POST.get('category')
            title = request.POST.get('title')
            banner = request.FILES.get('banner')

            if frm.is_valid():
                content = frm.cleaned_data['content']
                blog_obj.title = title,
                blog_obj.content = content,
                blog_obj.category = Category.objects.get(id = category)
                if banner:
                    blog_obj.image = banner
                blog_obj.save()
                return redirect('/profile')

        initial_dict = {'content' : blog_obj.content}
        frm = BlogForm(initial=initial_dict)
    except Exception as e:
        print(e)
    return render(request, 'blogs/create_blog.html',{
        'frm' : frm,
        'blog' : blog_obj,
        'categories' : category
    })


def delete_blog(request, id):
    blog = Blog.objects.get(id = id)
    blog.delete()
    return redirect('/profile')