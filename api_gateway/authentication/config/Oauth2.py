from authlib.integrations.starlette_client import OAuth

from api_gateway.settings import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'consent'
    }
)

oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={
        'scope': 'user:email read:user',
    },
)

oauth.register(
    name="twitter",
    client_id=settings.X_CLIENT_ID,
    client_secret=settings.X_CLIENT_SECRET,
    authorize_url="https://twitter.com/i/oauth2/authorize",
    access_token_url="https://api.x.com/2/oauth2/token",
    redirect_uri="http://docconvert.local:8000/twitter/callback",
    client_kwargs={
        "scope": "users.read tweet.read offline.access",
        "code_challenge_method": "S256",
    },
)
