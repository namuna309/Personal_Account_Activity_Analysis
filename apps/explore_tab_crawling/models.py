from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    hashtags = models.CharField(
        max_length=2000, null=False, verbose_name="해시태그")
    likes = models.IntegerField(default=0, null=False, verbose_name="좋아요수")
    comments = models.IntegerField(default=0, null=False, verbose_name="댓글수")
    slide = models.BooleanField(default=False, verbose_name='슬라이드여부')
    url = models.CharField(max_length=2000, null=False, verbose_name='주소')
    created_at = models.DateTimeField(null=False, verbose_name="작성일시")

    class Meta:
        db_table = 'content'

    def __str__(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M")


class Hashtag(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    content_id = models.ForeignKey(
        Content, null=False, on_delete=models.CASCADE, verbose_name="콘텐츠")
    text = models.CharField(max_length=200, verbose_name='단어')
    frequency = models.IntegerField(default=0, null=False, verbose_name="빈도수")

    class Meta:
        db_table = 'hashtag'
        constraints = [
            UniqueConstraint(fields=['content_id', 'text'],
                             name='unique_content_text')
        ]
