def process_stripe(payment):
    # integrate stripe SDK here
    payment.status = "success"
    payment.transaction_id = "STRIPE123456"
    payment.save()
    return True
    # return False in case of failure
    