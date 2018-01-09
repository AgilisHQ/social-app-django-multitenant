from setuptools import setup

setup(
    name='social-app-django-multitenant',
    version='0.1',
    install_requires=[
        'django==1.10.5',
        'social-auth-core==1.1.0',
        'social-auth-app-django==1.0.1',
        'django-tenant-schemas==1.6.11',
        'six>=1.10.0'
    ]
)
