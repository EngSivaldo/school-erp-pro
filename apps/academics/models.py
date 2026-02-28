from django.db import models
from apps.students.models import Student

class GradeLevel(models.Model):
    """Ex: 1º Ano, 2º Ano"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subject(models.Model):
    """Matérias: Matemática, Português"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    """Turma: 1º Ano A - 2026"""
    name = models.CharField(max_length=10)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    year = models.IntegerField()
    shift = models.CharField(max_length=20, choices=[('MANHA', 'Manhã'), ('TARDE', 'Tarde')])

    def __str__(self):
        return f"{self.grade_level.name} - {self.name} ({self.year})"

class Enrollment(models.Model): # <--- A CLASSE QUE ESTAVA FALTANDO
    """Vínculo de Matrícula"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='ACTIVE')

    class Meta:
        unique_together = ('student', 'classroom') # Impede matrícula dupla na mesma turma

    def __str__(self):
        return f"{self.student.user.get_full_name()} em {self.classroom}"