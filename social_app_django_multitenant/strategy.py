from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.functional import Promise
from django.utils.encoding import force_text

from social_core.utils import setting_name
from social_core.pipeline import DEFAULT_AUTH_PIPELINE, DEFAULT_DISCONNECT_PIPELINE
from social_django.strategy import DjangoStrategy


class DjangoMultiTenantStrategy(DjangoStrategy):
    """
    Custom social django strategy to support multitenant,
    We modify workflow to get social auth settings from Tenant model.
    Add this field to your django tenant schemas model:
    social_auth_settings = JsonField()
    """

    def __init__(self, storage, request, tpl=None):
        self.request = request
        self.session = request.session if request else {}
        super(DjangoMultiTenantStrategy, self).__init__(storage, request, tpl)

    def _get_tenant(self, request=None):
        '''
        Get tenant object. This query will always return one tenant.
        '''
        if request:
            return request.tenant

        return None

    def get_setting(self, name, backend=None):
        if backend and name.startswith('SOCIAL_AUTH'):
            tenant = self._get_tenant(self.request)
            try:
                value = tenant.social_auth_settings[
                    backend.name][name]

            except KeyError:
                value = tenant.social_auth_settings[name]

        else:
            value = getattr(settings, name)

        # Force text on URL named settings that are instance of Promise
        if name.endswith('_URL'):
            if isinstance(name, Promise):
                value = force_text(value)

            value = resolve_url(value)

        return value

    def setting(self, name, default=None, backend=None):
        names = [setting_name(name), name]
        if backend:
            names.insert(0, setting_name(backend.name, name))

        for name in names:
            try:
                return self.get_setting(name, backend)

            except (AttributeError, KeyError):
                pass

        return default

    def get_pipeline(self, backend=None, request=None):
        '''
        Modified get_pipeline method to make it get from each tenant
        We convert to tuple social auth settings from tenant because tuple is invalid JSON format
        '''
        tenant = self._get_tenant(request)
        if tenant:
            if 'SOCIAL_AUTH_PIPELINE' in tenant.social_auth_settings.keys():
                return tuple(tenant.social_auth_settings['SOCIAL_AUTH_PIPELINE'])

        return self.setting('PIPELINE', DEFAULT_AUTH_PIPELINE, backend)

    def get_disconnect_pipeline(self, backend=None):
        '''
        Modified get_disconnect_pipeline method to make it get from each tenant
        We convert to tuple social auth settings from tenant because tuple is invalid JSON format
        '''
        tenant = self._get_tenant(self.request)
        if tenant:
            if 'DISCONNECT_PIPELINE' in tenant.social_auth_settings.keys():
                return tuple(tenant.social_auth_settings['DISCONNECT_PIPELINE'])

        return self.setting('DISCONNECT_PIPELINE', DEFAULT_DISCONNECT_PIPELINE, backend)
