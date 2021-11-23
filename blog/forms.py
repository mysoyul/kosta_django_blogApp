from django import forms
from .models import Post

# Validator 함수 선언
# title 필드의 길이 체크 < 3

def min_length_3_validator(value):
    if len(value) < 3 :
        # Exception 강제로 발생시킬때는 raise 구문사용
        raise forms.ValidationError('title은 3글자 이상 입력해 주세요')
        
# PostForm 클래스 선언
class PostForm(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    text = forms.CharField(widget=forms.Textarea)