from django.conf import settings
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("rest_verify_email", kwargs={'key': emailconfirmation.key})
        ret = build_absolute_uri(request, url)
        return ret