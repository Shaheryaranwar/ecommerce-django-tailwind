def process_paypal(payment):
    payment.status = "success"
    payment.transaction_id = "PAYPAL123456"
    payment.save()
    return True
