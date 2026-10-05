from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in

        from .signals import merge_wishlist_on_login

        user_logged_in.connect(merge_wishlist_on_login)
