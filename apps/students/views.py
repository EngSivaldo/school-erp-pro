from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10 # Paginação automática

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Busca por nome ou matrícula
            queryset = queryset.filter(
                user__first_name__icontains=query
            ) | queryset.filter(registration_number__icontains=query)
        return queryset