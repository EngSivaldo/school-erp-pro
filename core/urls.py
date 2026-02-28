from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import DashboardView
from apps.students.views import StudentListView 
from apps.attendance.views import AttendanceSheetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('alunos/', StudentListView.as_view(), name='student-list'), 
    path('chamada/<int:classroom_id>/', AttendanceSheetView.as_view(), name='attendance-sheet'),
]