from django.db import models
from apps.students.models import Student
from apps.academics.models import Classroom, Subject

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'date') # Impede duplicar presença no mesmo dia

    def __str__(self):
        status = "Presente" if self.is_present else "Faltou"
        return f"{self.student} - {self.date}: {status}"