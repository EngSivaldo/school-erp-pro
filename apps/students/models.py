from django.db import models
from django.conf import settings

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_profile')
    cpf = models.CharField(max_length=14, unique=True)
    address = models.TextField()
    profession = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Resp: {self.user.get_full_name()}"

class Student(models.Model):  # <--- CERTIFIQUE-SE DE QUE ESTÁ ASSIM
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    guardians = models.ManyToManyField(Guardian, related_name='students')
    medical_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.registration_number} - {self.user.get_full_name()}"