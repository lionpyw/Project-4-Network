from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from .settings import api_settings


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    def dummy_get_response(request):  # pragma: no cover
            return None

    check = CSRFCheck(dummy_get_response)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            if not api_settings.AUTH_COOKIE:
                return None
            else:
                raw_token = request.COOKIES.get(api_settings.AUTH_COOKIE) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)
        if not user or not user.is_active:
            return None

        if api_settings.AUTH_COOKIE:
            enforce_csrf(request)

        return user, validated_token
    