def process_easypaisa(payment):
    payment.status = "success"
    payment.transaction_id = "EASYPaisa123"
    payment.save()
    return True
