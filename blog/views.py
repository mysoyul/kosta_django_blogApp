from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Post

# 글상세


# 글목록
def post_list(request):
    post_queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': post_queryset} )

def post_list_first(request):
    name = 'Django'
    return HttpResponse('''
        <h2>Welcome {name} </h2>
        <p>Http Method : {method}</p>
        <p>Http Encoding : {enc} </p>
        <p>Http Path : {path1} </p>
        '''.format(name=name, method=request.method, enc=request.encoding,
                   path1=request.path))
