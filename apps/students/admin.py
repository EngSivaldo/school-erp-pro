from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Usamos funções personalizadas para buscar dados da tabela User
    list_display = ('registration_number', 'get_name', 'get_email', 'is_active')
    search_fields = ('registration_number', 'user__first_name', 'user__email')

    @admin.display(description='Nome')
    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    @admin.display(description='E-mail')
    def get_email(self, obj):
        return obj.user.email