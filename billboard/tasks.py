from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

import datetime

from celery import shared_task

from bulletin_board import settings
from billboard.models import Article, Comment
from accounts.models import CustomUser


@shared_task
def weekly_notification():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    articles = set(Article.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')[:5])
    users = CustomUser.objects.all()
    subject = 'Еженедельная рассылка от MMO PORTAL!'
    html_content = render_to_string(
        'tasks/monday_mail_task.html',
        {
            'link': settings.SITE_URL,
            'articles': articles,
        }
    )
    for user in users:
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def comment_created(pk, **kwargs):

    comment = Comment.objects.get(pk=pk)
    email = comment.article.author.email
    html_content = render_to_string(
        template_name='tasks/comment_created_email.html',
        context={
            'article': comment.article,
            'text': comment.text,
            'link': f'http://127.0.0.1:8000/comment/filter',
        }
    )
    msg = EmailMultiAlternatives(
        subject=comment.text,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def accept_comment(pk, **kwargs):

    comment = Comment.objects.get(pk=pk)
    email = comment.author.email
    html_content = render_to_string(
        template_name='tasks/accept_comment_email.html',
        context={
            'text': comment.text,
            'link': f'http://127.0.0.1:8000//comment/User/',
        }
    )
    msg = EmailMultiAlternatives(
        subject=comment.text,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

