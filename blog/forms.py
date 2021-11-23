from django import forms
from .models import Post

#PostForm 클래스 선언
class PostForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)