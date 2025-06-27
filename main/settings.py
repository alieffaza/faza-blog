INSTALLED_APPS = [
    # ... aplikasi lain ...
    # 'social_django',
]

MIDDLEWARE = [
    # ... middleware lain ...
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
]

# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR_GOOGLE_CLIENT_ID'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'

# LOGIN_URL = 'login'
# LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'dashboard'
# LOGOUT_REDIRECT_URL = 'login'

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

AUTH0_DOMAIN = 'dev-bl2n0w4kngkr63pj.us.auth0.com'
AUTH0_CLIENT_ID = '3Z5QB900quXKeaKvY1CWnz8O6K2xYfE9'
AUTH0_CLIENT_SECRET = 'o8yaD___cpX00fFK3ofqrrLdDtWrwmWbBtEIcH8-dGJ7oI4EMAtfGYydRNY_Eu-g'
AUTH0_CALLBACK_URL = 'http://localhost:8000/auth/callback'

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]'] 