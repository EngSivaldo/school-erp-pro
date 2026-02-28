from django.db import models
from django.conf import settings

class Announcement(models.Model):
    """Mural de Avisos da Escola"""
    PRIORITY_CHOICES = [('LOW', 'Baixa'), ('NORMAL', 'Normal'), ('HIGH', 'Alta')]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NORMAL')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title