from django.urls import path
from .views import (
    InstallmentPayView,
    MercadoPagoWebhookView,
    StudentCreateView, 
    StudentListView, 
    StudentUpdateView, 
    StudentDetailView, 
    StudentFinanceView,
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('novo/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/editar/', StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/perfil/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/financeiro/', StudentFinanceView.as_view(), name='student_finance'),
    path('parcela/<int:pk>/pagar/', InstallmentPayView.as_view(), name='installment_pay'),
    path('webhook/mercadopago/', MercadoPagoWebhookView.as_view(), name='mp_webhook'),
]