from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.students.models import Student
from apps.academics.models import Classroom
from apps.finance.models import Invoice
from apps.communications.models import Announcement # <--- NOVO

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas Reais
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['total_classes'] = Classroom.objects.count()
        context['pending_invoices'] = Invoice.objects.filter(status='PENDING').count()
        
        # Avisos Reais da Secretaria
        # Pegamos os 5 últimos avisos ativos, do mais novo para o mais antigo
        context['recent_alerts'] = Announcement.objects.filter(active=True).order_by('-created_at')[:5]
        
        return context