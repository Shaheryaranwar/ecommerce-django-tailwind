def process_jazzcash(payment):
    payment.status = "success"
    payment.transaction_id = "JAZZCASH123"
    payment.save()
    return True
