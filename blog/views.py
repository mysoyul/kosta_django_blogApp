from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from .forms import PostForm, PostModelForm, CommentModelForm
from .models import Post, Comment

# 댓글승인
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.approve()
    return redirect('post_detail', pk=post_pk)

# 댓글삭제
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

# 댓글등록 (CommentModelForm 사용)
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # Comment와 Post 연결
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentModelForm()
    return render(request, 'blog/add_comment_to_post.html',{'form': form})

# 글삭제
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

# 글수정(PostModelForm사용)
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            # post = form.save(commit=True)

            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

# 글등록처리를 Class 기반으로 작성
class MyFormView(View):
    form_class = PostModelForm
    template_name = 'blog/post_edit.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect('/post/%i' % post.pk)

        return render(request, self.template_name, {'form': form})

# 글등록 (PostForm 사용)
@login_required
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
