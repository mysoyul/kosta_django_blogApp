from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm, PostModelForm
from .models import Post

# 글수정(PostModelForm사용)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

# 글등록 (PostForm 사용)
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        # Form의 데이터가 clean 한 상태인지 체크
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(
                author=User.objects.get(username=request.user),
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                published_date=timezone.now()
            )
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

# 글상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
