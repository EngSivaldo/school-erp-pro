from django.db import models
from apps.students.models import Student

class Invoice(models.Model):  # Verifique o nome aqui
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('OVERDUE', 'Atrasado'),
        ('CANCELLED', 'Cancelado'),
    ]

    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.description}"