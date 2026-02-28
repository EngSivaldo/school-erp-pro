from django.db import models
from apps.academics.models import Enrollment, Subject

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    period = models.IntegerField(choices=[(1, '1º Bimestre'), (2, '2º Bimestre'), (3, '3º Bimestre'), (4, '4º Bimestre')])

    class Meta:
        unique_together = ('enrollment', 'subject', 'period') # Um aluno não tem duas notas na mesma matéria no mesmo bimestre

    def __str__(self):
        return f"{self.enrollment.student} | {self.subject} | {self.period}º Bim: {self.value}"