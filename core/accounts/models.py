from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    PAPEL_CHOICES = [
        ('admin', 'Administrador'),
        ('encarregado', 'Encarregado'),
        ('operador', 'Operador'),
        ('mecanico', 'Mecânico'),
        ('gestor', 'Gestor'),   
    ]
    nome = models.CharField(max_length=100)
    papel = models.CharField(max_length=20, choices=PAPEL_CHOICES)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_active = self.ativo
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.papel})"
