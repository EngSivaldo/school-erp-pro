from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.academics.models import Enrollment, Classroom
from .models import Attendance
from datetime import date

class AttendanceSheetView(LoginRequiredMixin, View):
    def get(self, request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)
        # Procura todos os alunos matriculados nesta turma
        enrollments = Enrollment.objects.filter(classroom=classroom, status='ACTIVE')
        return render(request, 'attendance/attendance_sheet.html', {
            'enrollments': enrollments,
            'classroom': classroom,
            'today': date.today()
        })

    def post(self, request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)
        students_present = request.POST.getlist('present_students') # IDs dos alunos marcados
        enrollments = Enrollment.objects.filter(classroom=classroom, status='ACTIVE')

        for enrollment in enrollments:
            # Se o ID do aluno está na lista de presentes, is_present = True
            Attendance.objects.update_or_create(
                student=enrollment.student,
                classroom=classroom,
                date=date.today(),
                defaults={'is_present': str(enrollment.student.id) in students_present}
            )
        return redirect('dashboard')