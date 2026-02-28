from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Course

User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    # Campos do Usuário
    first_name = forms.CharField(label="Nome", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Lucas'}))
    last_name = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Almeida'}))
    email = forms.EmailField(label="E-mail Institucional", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'lucas@exemplo.com'}))

    class Meta:
        model = Student
        # Campos de endereço e curso que acabamos de criar no banco
        fields = [
            'course', 'birth_date', 'phone', 'cep', 'address', 
            'number', 'neighborhood', 'city', 'state', 'medical_notes'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_address'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_neighborhood'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_city', 'readonly': 'readonly'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_state', 'readonly': 'readonly'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }