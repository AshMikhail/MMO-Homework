from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


from accounts.models import CustomUser


class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CATEGORY = (
        ('TK', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('BU', 'Торговцы'),
        ('GM', 'Гильдмастеры'),
        ('QG', 'Квестгиверы'),
        ('BS', 'Кузнецы'),
        ('SK', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SM', 'Мастера заклинаний'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY, default='TK')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = RichTextUploadingField()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.article.id)])
