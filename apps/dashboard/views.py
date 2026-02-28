from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# O Dashboard "visita" os outros apps para pegar dados
from apps.students.models import Student
from apps.academics.models import Classroom
from apps.finance.models import Invoice
from apps.communications.models import Announcement

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # O Dashboard consolida tudo aqui
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['total_classes'] = Classroom.objects.count()
        context['pending_invoices'] = Invoice.objects.filter(status='PENDING').count()
        context['recent_alerts'] = Announcement.objects.filter(active=True).order_by('-created_at')[:5]
        
        return context