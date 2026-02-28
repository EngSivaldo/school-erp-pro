from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Invoice

class FinanceService:
    @staticmethod
    def generate_annual_invoices(student, monthly_value, start_date):
        """Gera 12 mensalidades para um aluno a partir de uma data inicial"""
        invoices = []
        for i in range(12):
            due_date = start_date + relativedelta(months=i)
            invoice = Invoice(
                student=student,
                description=f"Mensalidade {due_date.month}/{due_date.year}",
                amount=monthly_value,
                due_date=due_date,
                status='PENDING'
            )
            invoices.append(invoice)
        
        # Salva tudo de uma vez no banco (Performance Sênior)
        Invoice.objects.bulk_create(invoices)
        return len(invoices)