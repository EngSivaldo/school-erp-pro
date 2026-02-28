from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Definimos os papéis (RBAC)
    ADMIN = 'ADMIN'
    SECRETARIA = 'SECRETARIA'
    PROFESSOR = 'PROFESSOR'
    FINANCEIRO = 'FINANCEIRO'
    ALUNO = 'ALUNO'
    RESPONSAVEL = 'RESPONSAVEL'
    DIRECAO = 'DIRECAO'

    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (SECRETARIA, 'Secretaria'),
        (PROFESSOR, 'Professor'),
        (FINANCEIRO, 'Financeiro'),
        (ALUNO, 'Aluno'),
        (RESPONSAVEL, 'Responsável'),
        (DIRECAO, 'Direção'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ALUNO)
    phone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, null=True)

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_staff_member(self):
        """Helper para verificar se é funcionário"""
        return self.role in [self.ADMIN, self.SECRETARIA, self.FINANCEIRO, self.DIRECAO]