from django.contrib.auth.models import AbstractUser
from django.db import models
import requests

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class FavoriteStock(models.Model):
    user = models.ForeignKey('User', related_name='favorite_stocks', on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stock_symbol

