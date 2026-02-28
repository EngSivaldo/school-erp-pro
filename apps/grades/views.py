from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grade
from apps.academics.models import Enrollment

class ReportCardView(LoginRequiredMixin, ListView):
    template_name = 'grades/report_card.html'
    context_object_name = 'grades'

    def get_queryset(self):
        # Se for aluno, vê as próprias notas. Se for admin, passamos o id via URL.
        student_id = self.kwargs.get('student_id')
        if not student_id and hasattr(self.request.user, 'student_profile'):
            student_id = self.request.user.student_profile.id
            
        return Grade.objects.filter(enrollment__student_id=student_id).order_by('subject', 'period')