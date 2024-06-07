from django_filters import FilterSet
from .models import Article, Comment


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = [
            'category',
        ]

class UserCommentFilter(FilterSet):
    class Meta:
        model = Article
        fields = [
            'text',
        ]


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'article'
        ]

    def __init__(self, *args, **kwargs):
        super(CommentFilter, self).__init__(*args, **kwargs)
        self.filters['article'].queryset = Article.objects.filter(author__username=kwargs['request'])