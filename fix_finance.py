import os
import django
from datetime import date
from dateutil.relativedelta import relativedelta

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.students.models import Student, Installment

def generate_missing_installments():
    students = Student.objects.all()
    created_count = 0

    print("--- Iniciando Atualização Financeira ---")

    for student in students:
        # Verifica se o aluno já tem parcelas para não duplicar
        if not student.installments.exists():
            parcelas = []
            # Define a data base (mês atual)
            data_base = date.today().replace(day=10) 
            
            for i in range(1, 13):
                parcelas.append(Installment(
                    student=student,
                    number=i,
                    value=450.00,
                    due_date=data_base + relativedelta(months=i-1)
                ))
            
            Installment.objects.bulk_create(parcelas)
            print(f"✅ Parcelas geradas para: {student.user.get_full_name()}")
            created_count += 1
    
    print(f"--- Finalizado! {created_count} alunos atualizados. ---")

if __name__ == "__main__":
    generate_missing_installments()