from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'subject', 'period', 'value')
    list_filter = ('period', 'subject')
    search_fields = ('enrollment__student__user__first_name',)