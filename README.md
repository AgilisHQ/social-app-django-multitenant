###Configuration

- Add social_app_django_multitenant to INSTALLED_APPS
- Add SOCIAL_AUTH_STRATEGY = 'social_app_django_multitenant.strategy.DjangoMultiTenantStrategy' to django settings
- Add social_auth_settings = JsonField() to your Tenant model
- Add social auth settings with this format
  {"linkedin": [{"SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY": ""}, {"SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET": ""}]}