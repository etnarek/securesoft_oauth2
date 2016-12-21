DEBUG = True
SECRET = "s3cr3t"

OAUTH_ID = "HXt0flfcF8ogoWn0iEWLiTV7toYOhH5QbO2ByKr8"
OAUTH_SECRET = "TrnUW0AcxvJxZc2PQ40cBohcM84hQNZ9GQYaDboMQS7PFsoHxTDilI7RcHqKPieQlYZtHihxcAM5drHBBjSPxNE4BGAA6trmQOKZUg4CE0NEmG1T9rhaaLZGWzcmRaxe"
SERVER_URL = "https://oauthserver.etnarek.com/"
TOKEN_URL = "o/token/"
AUTHORIZATION_URL = "o/authorize"

try:
    from local_config import *
except ImportError:
    print("No local config found!")
