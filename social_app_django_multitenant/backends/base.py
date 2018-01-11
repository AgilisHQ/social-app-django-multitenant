from social_core.backends.base import BaseAuth as AbstractBaseAuth


class BaseAuth(AbstractBaseAuth):

    def authenticate(self, *args, **kwargs):
        '''
        Modified method to support multitenant
        We pass request object to get_pipeline()
        '''
        if 'backend' not in kwargs or kwargs['backend'].name != self.name or \
           'strategy' not in kwargs or 'response' not in kwargs:
            return None

        self.strategy = self.strategy or kwargs.get('strategy')
        self.redirect_uri = self.redirect_uri or kwargs.get('redirect_uri')
        self.data = self.strategy.request_data()
        kwargs.setdefault('is_new', False)
        pipeline = self.strategy.get_pipeline(
            self, request=kwargs['strategy'].request)
        args, kwargs = self.strategy.clean_authenticate_args(*args, **kwargs)
        return self.pipeline(pipeline, *args, **kwargs)
