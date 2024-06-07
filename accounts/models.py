from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pcc = models.CharField(max_length=6, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('User', args=[str(self.id)])

