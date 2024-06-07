from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy



from .models import Article, Comment
from accounts.models import CustomUser
from .forms import ArticleForm, Comment_Form
from .filters import ArticleFilter, CommentFilter, UserCommentFilter
from .tasks import comment_created, accept_comment




class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'billboard/article_all.html'
    context_object_name = 'all_articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class UserArticleList(View):
    def get(self, request):
        current_user = request.user
        user = current_user
        try:
            author = CustomUser.objects.get(username=user)
        except CustomUser.DoesNotExist:
            return redirect('all_articles')
        else:
            article = Article.objects.filter(author=author)
            filterset = ArticleFilter(self.request.GET, queryset=article)
            return render(request, 'account/Users.html', context={'filterset': filterset})


class ArticleDetail(DetailView):
    model = Article
    template_name = 'billboard/article_detail.html'
    context_object_name = 'article'


class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Article
    template_name = 'billboard/article_edit.html'

    def form_valid(self, form):
            article = form.save(commit=False)
            form.instance.author = CustomUser.objects.get(id=self.request.user.id)
            article.save()
            return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = 'billboard.change_article'
    form_class = ArticleForm
    model = Article
    template_name = 'billboard/article_edit.html'

    def form_valid(self, form):
        obj = self.get_object()
        if obj.author == self.request.user:
            article = form.save(commit=False)
            form.instance.author = CustomUser.objects.get(id=self.request.user.id)
            article.save()
            return super().form_valid(form)
        else:
            raise PermissionDenied

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'billboard/article_delete.html'
    success_url = reverse_lazy('User')

    def form_valid(self, form):
        obj = self.get_object()
        if obj.author == self.request.user:
            return super().form_valid(form)
        else:
            raise PermissionDenied


class UserCommentList(View):
    def get(self, request):
        user = request.user
        try:
            author = CustomUser.objects.get(username=user)
        except CustomUser.DoesNotExist:
            return redirect('all_articles')
        else:
            comment = Comment.objects.filter(author=author)
            filterset = UserCommentFilter(self.request.GET, queryset=comment)
            return render(request, 'billboard/comment_user.html', context={'filterset': filterset})

class CommentListFilter(ListView):
    model = Comment
    template_name = 'billboard/comment_filter.html'

    def get_queryset(self):
        queryset = Comment.objects.filter(article__author__username=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CommentDetail(DetailView):
    model = Comment
    template_name = 'billboard/comment_detail.html'
    context_object_name = 'comment'


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = Comment_Form
    model = Comment
    template_name = 'billboard/article_edit.html'

    def form_valid(self, form, *args, **kwargs):
        comment = form.save(commit=False)
        form.instance.author = CustomUser.objects.get(id=self.request.user.id)
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        author_comment = CustomUser.objects.get(id=self.request.user.id)
        if author_comment == comment.article.author:
            comment.status = True
            comment.save()
        else:
            comment.save()
            comment_created.delay(comment.pk)
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = 'billboard.change_comment'
    form_class = Comment_Form
    model = Comment
    template_name = 'billboard/article_edit.html'

    def form_valid(self, form):
        obj = self.get_object()
        if obj.author == self.request.user:
            comment = form.save(commit=False)
            form.instance.author = CustomUser.objects.get(id=self.request.user.id)
            comment.save()
            return super().form_valid(form)
        else:
            raise PermissionDenied

def comment_accept(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.status = True
    comment.save()
    accept_comment.delay(comment.pk)
    return redirect('all_comments')


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'billboard/comment_delete.html'
    success_url = reverse_lazy('all_comments')