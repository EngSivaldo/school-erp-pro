import datetime
from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Curso")
    code = models.CharField(max_length=10, unique=True, verbose_name="Sigla/Código")
    description = models.TextField(blank=True, verbose_name="Descrição")

    def __str__(self):
        return self.name

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_profile')
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    profession = models.CharField(max_length=100, blank=True)
    # Endereço do Responsável
    cep = models.CharField(max_length=9, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"Resp: {self.user.get_full_name()}"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='students', verbose_name="Curso")
    phone = models.CharField(max_length=20, verbose_name="Telefone", default='0000000000')
    # Gerado pelo sistema (Nível Enterprise)
    registration_number = models.CharField(max_length=20, unique=True, editable=False)
    
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    guardians = models.ManyToManyField(Guardian, related_name='students', verbose_name="Responsáveis")
    medical_notes = models.TextField(blank=True, verbose_name="Observações Médicas")
    
    # Endereço do Aluno (pode ser diferente do responsável)
    cep = models.CharField(max_length=9)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.registration_number:
            year = datetime.date.today().year
            # Conta quantos alunos existem no ano atual para o sequencial
            count = Student.objects.filter(registration_number__startswith=str(year)).count()
            self.registration_number = f"{year}{(count + 1):04d}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-registration_number']

    def __str__(self):
        return f"{self.registration_number} - {self.user.get_full_name()}"
    


class Installment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='installments')
    number = models.PositiveIntegerField("Número da Parcela")
    value = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    due_date = models.DateField("Data de Vencimento")
    is_paid = models.BooleanField("Pago", default=False)
    payment_date = models.DateField("Data do Pagamento", null=True, blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.student.user.first_name} - Parcela {self.number}"