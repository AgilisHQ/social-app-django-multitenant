from functools import wraps

from django.core.urlresolvers import reverse
from django.http import Http404

from social_core.exceptions import MissingBackend
from social_core.utils import parse_qs, constant_time_compare, handle_http_errors, url_add_parameters, cache
from social_django.utils import load_backend, load_strategy, BackendWrapper


def psa(redirect_uri=None, load_strategy=load_strategy):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))

            request.social_strategy = load_strategy(request)
            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, 'strategy'):
                request.strategy = request.social_strategy

            try:
                request.backend = load_backend(request.social_strategy,
                                               backend, uri)
            except MissingBackend:
                raise Http404('Backend not found')
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator
