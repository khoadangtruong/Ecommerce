from django.shortcuts import render
from blog.models import Blog
from django.core.paginator import Paginator

# Create your views here.
def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')[:9]
    paginator = (Paginator(blogs, 6))
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {
        'blogs': blogs,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, id):
    blog = Blog.objects.get(pk = id)
    context = {
        'blog': blog,
    }
    return render(request, 'blog_detail.html', context)
