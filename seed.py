import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.students.models import Student
from apps.academics.models import Classroom, GradeLevel, Enrollment

def run_seed():
    User = get_user_model()
    
    # 1. Criar Turma
    gl, _ = GradeLevel.objects.get_or_create(name="1º Ano")
    classroom, _ = Classroom.objects.get_or_create(
        name="A", grade_level=gl, year=2026, shift="MANHA"
    )

    # 2. Criar Usuário e Aluno
    user_student, created = User.objects.get_or_create(
        username='aluno_teste', 
        defaults={'first_name': 'João', 'last_name': 'Exemplo', 'role': 'STUDENT'}
    )
    if created:
        user_student.set_password('senha123')
        user_student.save()

    student, _ = Student.objects.get_or_create(
        user=user_student,
        defaults={'registration_number': '2026001', 'birth_date': '2015-01-01'}
    )

    # 3. Matricular
    Enrollment.objects.get_or_create(student=student, classroom=classroom)
    
    print("✅ Banco de dados sincronizado e Aluno matriculado!")

if __name__ == "__main__":
    run_seed()