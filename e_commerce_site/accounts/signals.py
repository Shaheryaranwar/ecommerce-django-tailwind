from wishlist.utils import merge_session_wishlist


def merge_wishlist_on_login(sender, request, user, **kwargs):
    merge_session_wishlist(request, user)
