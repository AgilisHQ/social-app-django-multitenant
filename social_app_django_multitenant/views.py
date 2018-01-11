from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache

from social_core.utils import setting_name
from social_core.actions import do_auth, do_complete, do_disconnect
from social_django.views import _do_login
from .utils import psa


NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'


@never_cache
@psa('{0}:complete'.format(NAMESPACE))
def auth(request, backend):
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, request=request, *args, **kwargs)


@never_cache
@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(request.backend, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)
