import mercadopago
from django.conf import settings

def gerar_link_pagamento(installment):
    """
    O propósito desta função é enviar os dados da parcela 
    para o Mercado Pago e receber um link de checkout.
    """
    # 1. Configuramos o SDK com seu Token (mesmo que seja o de teste depois)
    sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

    # 2. Criamos os dados da 'Preferência' (o que o aluno vai pagar)
    preference_data = {
        "items": [
            {
                "title": f"Mensalidade {installment.number}/12 - {installment.student.user.get_full_name()}",
                "quantity": 1,
                "unit_price": float(installment.value),
            }
        ],
        "external_reference": str(installment.id), # Para sabermos qual parcela foi paga depois
    }

    # 3. Enviamos para o Mercado Pago
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    # 4. Retornamos o link que o aluno vai clicar
    return preference["sandbox_init_point"] # Link de teste