def process_cod(payment):
    payment.status = "success"
    payment.transaction_id = "COD"
    payment.save()
    return True
