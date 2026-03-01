from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import transaction
from datetime import date
from dateutil.relativedelta import relativedelta # Para pular meses com precisão

from .models import Student, Installment # Certifique-se de ter criado o model Installment
from .forms import StudentRegistrationForm

User = get_user_model()

# --- LISTAGEM ---
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                user__first_name__icontains=query
            ) | queryset.filter(registration_number__icontains=query)
        return queryset

# --- CRIAÇÃO COM GERAÇÃO DE PARCELAS ---
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # 1. Criação do Usuário
                email = form.cleaned_data['email']
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password='aluno123@change',
                    role='STUDENT'
                )
                
                # 2. Salva o Aluno
                form.instance.user = user
                student = form.save()

                # 3. GERAÇÃO AUTOMÁTICA DE 12 PARCELAS
                parcelas = []
                data_vencimento_base = date.today() + relativedelta(months=1) # Primeira parcela para daqui a 30 dias
                
                for i in range(1, 13):
                    parcelas.append(Installment(
                        student=student,
                        number=i,
                        value=450.00, # Valor sugerido da mensalidade
                        due_date=data_vencimento_base + relativedelta(months=i-1)
                    ))
                
                # Salva todas de uma vez no banco (mais rápido)
                Installment.objects.bulk_create(parcelas)

                messages.success(self.request, f"Matrícula {student.registration_number} e 12 parcelas geradas!")
                return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Erro crítico: {str(e)}")
            return self.form_invalid(form)

# --- EDIÇÃO ---
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

# --- PERFIL ---
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

# --- FINANCEIRO (EXTRATO) ---
from django.db.models import Sum # Importante para somar os valores

class StudentFinanceView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_finance.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. Pegamos todas as parcelas
        installments = self.object.installments.all().order_by('due_date')
        
        # 2. Calculamos o Total do Contrato (Soma de todas as parcelas)
        total_contrato = installments.aggregate(total=Sum('value'))['total'] or 0
        
        # 3. Calculamos o Total Pago (Soma apenas das pagas)
        total_pago = installments.filter(is_paid=True).aggregate(total=Sum('value'))['total'] or 0
        
        context['installments'] = installments
        context['total_contrato'] = total_contrato
        context['total_pago'] = total_pago
        return context
    

# from django.shortcuts import get_object_or_404, redirect
# from django.views import View

# class InstallmentPayView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         # O propósito aqui é localizar a parcela pelo ID (pk)
#         installment = get_object_or_404(Installment, pk=pk)
        
#         # Mudamos o status e gravamos a data atual
#         installment.is_paid = True
#         installment.payment_date = date.today()
#         installment.save()
        
#         messages.success(request, f"Parcela {installment.number} baixada com sucesso!")
        
#         # Retorna para a página do financeiro do aluno correspondente
#         return redirect('student_finance', pk=installment.student.pk)



import uuid # Para gerar um código de transação único
from django.shortcuts import get_object_or_404, redirect
from .models import Installment

class InstallmentPayView(LoginRequiredMixin, View):
    """
    O propósito desta View é simular o que o Mercado Pago faz:
    Recebe a parcela e gera um link para o aluno pagar.
    """
    def post(self, request, pk):
        installment = get_object_or_404(Installment, pk=pk)
        
        # Simulando a resposta do Mercado Pago
        # No futuro, aqui chamaremos a função sdk.preference().create()
        payment_id = str(uuid.uuid4()) # ID fictício da transação
        
        # Link de Checkout Simulado (Pode ser uma página externa ou interna)
        # Por enquanto, vamos redirecionar para uma página de 'Processando'
        messages.info(request, f"Link de pagamento gerado para a parcela {installment.number}!")
        
        # Guardamos o ID da transação na parcela (opcional)
        # installment.transaction_id = payment_id
        # installment.save()
        
        return redirect('student_finance', pk=installment.student.pk)
    

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch') # O propósito é permitir que o Mercado Pago envie dados sem erro de segurança CSRF
class MercadoPagoWebhookView(View):
    def post(self, request, *args, **kwargs):
        try:
            # 1. Lemos o sinal enviado pelo Mercado Pago
            data = json.loads(request.body)
            
            # O propósito aqui é filtrar apenas avisos de 'payment' (pagamento)
            if data.get("type") == "payment":
                payment_id = data.get("data", {}).get("id")
                
                # SIMULAÇÃO: No mundo real, aqui usaríamos o SDK para consultar o status
                # preference_id = sdk.payment().get(payment_id)
                
                # 2. Localizamos a parcela (estamos usando um exemplo fixo para teste)
                # No real, buscaríamos pelo 'external_reference' que enviamos na criação
                installment = Installment.objects.filter(is_paid=False).first()
                
                if installment:
                    installment.is_paid = True
                    installment.payment_date = date.today()
                    installment.save()
                    print(f"✅ Webhook: Parcela {installment.id} confirmada com sucesso!")

            return HttpResponse(status=200) # O propósito é dizer ao MP: 'Recebi a mensagem!'
        except Exception as e:
            print(f"❌ Erro no Webhook: {e}")
            return HttpResponse(status=500)