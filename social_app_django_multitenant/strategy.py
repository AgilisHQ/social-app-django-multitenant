from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.functional import Promise
from django.utils.encoding import force_text

from social_core.utils import setting_name
from social_django.strategy import DjangoStrategy


class DjangoMultiTenantStrategy(DjangoStrategy):
    """
    Custom social django strategy to support multitenant,
    We modify workflow to get social auth settings from Tenant model.
    Add this field to your django tenant schemas model:
    social_auth_settings = JsonField()
    """

    def get_setting(self, name, backend=None):
        if backend and not name.endswith('_URL'):
            value = self.request.tenant.social_auth_settings[
                backend.name][name]

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
