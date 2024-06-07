from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'category',
            'title',
            'text',
        ]

class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]