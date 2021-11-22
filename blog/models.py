from django.db import models
from django.utils import timezone

class Post(models.Model):
    #작성자
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    #글제목
    title = models.CharField(max_length=200)
    #글내용
    text = models.TextField()

    #글작성일
    created_date = models.DateTimeField(default=timezone.now)
    #글게시일
    published_date = models.DateTimeField(blank=True, null=True)

    #삭제할 예정
    #content = models.TextField()

    #default로 title 필드를 반환 해주도록 부모 Model 클래스의 메서드 재정의
    def __str__(self):
        #return '%s object (%s)' % (self.__class__.__name__, self.pk)
        return f'{self.title} ({self.pk}) '
            #str(self.pk) + self.title

    #글게시일 필드에 현재날짜는 저장해주는 메서드
    def publish(self):
        self.published_date = timezone.now()
        self.save()


