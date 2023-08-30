import os

import environ

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    NEODB_DEBUG=(str, ""),
    # DB
    NEODB_DB_URL=(str, "postgres://neodb:aubergine@127.0.0.1:5432/neodb"),
    TAKAHE_DB_URL=(str, "postgres://takahe:takahepass@127.0.0.1:5432/takahe"),
    # REDIS
    NEODB_REDIS_HOST=(str, "127.0.0.1"),
    NEODB_REDIS_PORT=(int, 6379),
    NEODB_REDIS_DB=(int, 0),
    # TYPESENSE
    NEODB_TYPESENSE_ENABLE=(str, ""),
    NEODB_TYPESENSE_KEY=(str, "insecure"),
    NEODB_TYPESENSE_HOST=(str, "127.0.0.1"),
    NEODB_TYPESENSE_PORT=(str, "8108"),
    # SITE INFO
    NEODB_SITE_LOGO=(str, "/s/img/logo.svg"),
    NEODB_SITE_ICON=(str, "/s/img/logo.svg"),
    NEODB_USER_ICON=(str, "/s/img/avatar.svg"),
    # ADMIN_USERS
    NEODB_ADMIN_USERNAMES=(str, ""),
    # THIRD PARTY CREDENTIALS
    SPOTIFY_CREDENTIAL=(str, "***REMOVED***"),
    TMDB_API3_KEY=(str, "***REMOVED***"),
    GOOGLE_API_KEY=(str, "***REMOVED***"),
    DISCOGS_API_KEY=(str, "***REMOVED***"),
    IGDB_CLIENT_ID=(str, "deadbeef"),
    IGDB_CLIENT_SECRET=(str, "***REMOVED***"),
    # PROXY
    NEODB_DOWNLOADER_PROXY_LIST=(str, ""),
    NEODB_DOWNLOADER_BACKUP_PROXY=(str, ""),
    # STATIC/MEDIA ROOT & URL
    NEODB_STATIC_ROOT=(str, os.path.join(BASE_DIR, "static/")),
    TAKAHE_MEDIA_URL=(str, "/media/"),
    TAKAHE_MEDIA_ROOT=(str, "media"),
    NEODB_MEDIA_ROOT=(str, os.path.join(BASE_DIR, "media")),
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ====== USER CONFIGUTRATION START ======
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("NEODB_DEBUG")

# SECURITY WARNING: use your own secret key and keep it!
SECRET_KEY = env("NEODB_SECRET_KEY")

DATABASES = {
    "default": {
        "TEST": {
            "DEPENDENCIES": ["takahe"],
        },
        **env.db("NEODB_DB_URL"),
    },
    "takahe": env.db("TAKAHE_DB_URL"),
}


SEARCH_BACKEND = None
if env("NEODB_TYPESENSE_ENABLE"):
    SEARCH_BACKEND = "TYPESENSE"

# SEARCH_BACKEND = 'MEILISEARCH'
# MEILISEARCH_SERVER = 'http://127.0.0.1:7700'
# MEILISEARCH_KEY = 'deadbeef'

TYPESENSE_CONNECTION = {
    "api_key": env("NEODB_TYPESENSE_KEY"),
    "nodes": [
        {
            "host": env("NEODB_TYPESENSE_HOST"),
            "port": env("NEODB_TYPESENSE_PORT"),
            "protocol": "http",
        }
    ],
    "connection_timeout_seconds": 2,
}

SITE_DOMAIN = env("NEODB_SITE_DOMAIN")
SITE_INFO = {
    "site_name": env("NEODB_SITE_NAME"),
    "site_domain": SITE_DOMAIN,
    "site_url": f"https://{SITE_DOMAIN}",
    "site_logo": env("NEODB_SITE_LOGO"),
    "site_icon": env("NEODB_SITE_ICON"),
    "user_icon": env("NEODB_USER_ICON"),
    "social_link": "https://donotban.com/@testie",
    "support_link": "https://github.com/doubaniux/boofilsic/issues",
    "donation_link": "https://patreon.com/tertius",
}

SETUP_ADMIN_USERNAMES = [u for u in env("NEODB_ADMIN_USERNAMES").split(",") if u]

# Mastodon/Pleroma instance allowed to login, keep empty to allow any instance to login
MASTODON_ALLOWED_SITES = []

# Allow user to create account with email (and link to Mastodon account later)
ALLOW_EMAIL_ONLY_ACCOUNT = False

# Timeout of requests to Mastodon, in seconds
MASTODON_TIMEOUT = 30

MASTODON_CLIENT_SCOPE = "read:accounts read:follows read:search read:blocks read:mutes write:statuses write:media"
# use the following to avoid re-authorize when migrating to a future version with more features
# MASTODON_CLIENT_SCOPE = "read write follow"

# some Mastodon-compatible software like Pixelfed does not support granular scopes
MASTODON_LEGACY_CLIENT_SCOPE = "read write follow"

# Emoji code in mastodon
STAR_SOLID = ":star_solid:"
STAR_HALF = ":star_half:"
STAR_EMPTY = ":star_empty:"

DISCORD_WEBHOOKS = {"user-report": None}

# Spotify credentials
SPOTIFY_CREDENTIAL = env("SPOTIFY_CREDENTIAL")

# The Movie Database (TMDB) API Keys
TMDB_API3_KEY = env("TMDB_API3_KEY")
# TMDB_API4_KEY = "deadbeef.deadbeef.deadbeef"

# Google Books API Key
GOOGLE_API_KEY = env("GOOGLE_API_KEY")

# Discogs API Key
# How to get: a personal access token from https://www.discogs.com/settings/developers
DISCOGS_API_KEY = env("DISCOGS_API_KEY")

# IGDB
IGDB_CLIENT_ID = env("IGDB_CLIENT_ID")
IGDB_CLIENT_SECRET = env("IGDB_CLIENT_SECRET")

# List of available proxies for proxy downloader, in format of ["http://x.y:port?url=__URL__", ...]
DOWNLOADER_PROXY_LIST = [u for u in env("NEODB_DOWNLOADER_PROXY_LIST").split(",") if u]

# Backup proxy for proxy downloader, in format of "http://xyz:port?url=__URL__"
DOWNLOADER_BACKUP_PROXY = env("NEODB_DOWNLOADER_BACKUP_PROXY")

# Timeout of downloader requests, in seconds
DOWNLOADER_REQUEST_TIMEOUT = 90
# Timeout of downloader cache, in seconds
DOWNLOADER_CACHE_TIMEOUT = 300
# Number of retries of downloader, when site is using RetryDownloader
DOWNLOADER_RETRIES = 3

# ====== USER CONFIGUTRATION END ======

NEODB_VERSION = "0.8"
DATABASE_ROUTERS = ["takahe.db_routes.TakaheRouter"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# for legacy deployment:
# DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ALLOWED_HOSTS = ["*"]

# To allow debug in template context
# https://docs.djangoproject.com/en/3.1/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    # "maintenance_mode",  # this has to be first if enabled
    "django.contrib.admin",
    "hijack",
    "hijack.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",
    "django_rq",
    "django_bleach",
    "django_jsonform",
    "tz_detect",
    "sass_processor",
    "auditlog",
    "markdownx",
    "polymorphic",
    "easy_thumbnails",
    "user_messages",
    # "anymail",
    # "silk",
]

INSTALLED_APPS += [
    "management.apps.ManagementConfig",
    "mastodon.apps.MastodonConfig",
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "catalog.apps.CatalogConfig",
    "journal.apps.JournalConfig",
    "social.apps.SocialConfig",
    "developer.apps.DeveloperConfig",
    "takahe.apps.TakaheConfig",
    "legacy.apps.LegacyConfig",
]

INSTALLED_APPS += [  # we may override templates in these 3rd party apps
    "oauth2_provider",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "silk.middleware.SilkyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    # "maintenance_mode.middleware.MaintenanceModeMiddleware",  # this should be last if enabled
]

ROOT_URLCONF = "boofilsic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                # 'django.contrib.messages.context_processors.messages',
                "user_messages.context_processors.messages",
                "boofilsic.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "boofilsic.wsgi.application"

SESSION_COOKIE_NAME = "neodbsid"

AUTHENTICATION_BACKENDS = [
    "mastodon.auth.OAuth2Backend",
    "oauth2_provider.backends.OAuth2Backend",
]


MARKDOWNX_MARKDOWNIFY_FUNCTION = "journal.models.render_md"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

if os.getenv("NEODB_SSL", "") != "":
    # FIXME: remove this since user may enforce SSL in reverse proxy
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000

STATIC_URL = "/s/"
STATIC_ROOT = env("NEODB_STATIC_ROOT")
if DEBUG:
    # django-sass-processor will generate neodb.css on-the-fly when DEBUG
    # NEODB_STATIC_ROOT is readonly in docker mode, so we give it a writable place
    SASS_PROCESSOR_ROOT = "/tmp"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

AUTH_USER_MODEL = "users.User"

SILENCED_SYSTEM_CHECKS = [
    "admin.E404",  # Required by django-user-messages
    "models.W035",  # Required by takahe: identical table name in different database
    "fields.W344",  # Required by takahe: identical table name in different database
]

TAKAHE_MEDIA_URL = env("TAKAHE_MEDIA_URL")
TAKAHE_MEDIA_ROOT = env("TAKAHE_MEDIA_ROOT")
MEDIA_URL = "/m/"
MEDIA_ROOT = env("NEODB_MEDIA_ROOT")
STORAGES = {  # TODO: support S3
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    "takahe": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": TAKAHE_MEDIA_ROOT,
            "base_url": TAKAHE_MEDIA_URL,
        },
    },
}

# Allow user to login via any Mastodon/Pleroma sites
MASTODON_ALLOW_ANY_SITE = False if MASTODON_ALLOWED_SITES else True

REDIRECT_URIS = SITE_INFO["site_url"] + "/account/login/oauth"
# for sites migrated from previous version, either wipe mastodon client ids or use:
# REDIRECT_URIS = f'{SITE_INFO["site_url"]}/users/OAuth2_login/'

CSRF_TRUSTED_ORIGINS = [SITE_INFO["site_url"]]
if DEBUG:
    CSRF_TRUSTED_ORIGINS += ["http://127.0.0.1:8000", "http://localhost:8000"]

# Path to save report related images, ends with slash
REPORT_MEDIA_PATH_ROOT = "report/"
MARKDOWNX_MEDIA_PATH = "review/"
BOOK_MEDIA_PATH_ROOT = "book/"
DEFAULT_BOOK_IMAGE = os.path.join(BOOK_MEDIA_PATH_ROOT, "default.svg")
MOVIE_MEDIA_PATH_ROOT = "movie/"
DEFAULT_MOVIE_IMAGE = os.path.join(MOVIE_MEDIA_PATH_ROOT, "default.svg")
SONG_MEDIA_PATH_ROOT = "song/"
DEFAULT_SONG_IMAGE = os.path.join(SONG_MEDIA_PATH_ROOT, "default.svg")
ALBUM_MEDIA_PATH_ROOT = "album/"
DEFAULT_ALBUM_IMAGE = os.path.join(ALBUM_MEDIA_PATH_ROOT, "default.svg")
GAME_MEDIA_PATH_ROOT = "game/"
DEFAULT_GAME_IMAGE = os.path.join(GAME_MEDIA_PATH_ROOT, "default.svg")
COLLECTION_MEDIA_PATH_ROOT = "collection/"
DEFAULT_COLLECTION_IMAGE = os.path.join(COLLECTION_MEDIA_PATH_ROOT, "default.svg")
SYNC_FILE_PATH_ROOT = "sync/"
EXPORT_FILE_PATH_ROOT = "export/"

# Default redirect loaction when access login required view
LOGIN_URL = "/account/login"

# Admin site root url
ADMIN_URL = "tertqX7256n7ej8nbv5cwvsegdse6w7ne5rHd"

BLEACH_STRIP_COMMENTS = True
BLEACH_STRIP_TAGS = True

# Thumbnail setting
# It is possible to optimize the image size even more: https://easy-thumbnails.readthedocs.io/en/latest/ref/optimize/
THUMBNAIL_ALIASES = {
    "": {
        "normal": {
            "size": (200, 200),
            "crop": "scale",
            "autocrop": True,
        },
    },
}
# THUMBNAIL_PRESERVE_EXTENSIONS = ('svg',)
if DEBUG:
    THUMBNAIL_DEBUG = True

REDIS_HOST = env("NEODB_REDIS_HOST")
REDIS_PORT = int(env("NEODB_REDIS_PORT"))
REDIS_DB = int(env("NEODB_REDIS_DB"))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

RQ_QUEUES = {
    q: {
        "HOST": REDIS_HOST,
        "PORT": REDIS_PORT,
        "DB": REDIS_DB,
        "DEFAULT_TIMEOUT": -1,
    }
    for q in ["mastodon", "export", "import", "fetch", "crawl", "ap"]
}

RQ_SHOW_ADMIN_LINK = True

SEARCH_INDEX_NEW_ONLY = False

TYPESENSE_INDEX_NAME = "catalog"

DOWNLOADER_SAVEDIR = None

DISABLE_MODEL_SIGNAL = False  # disable index and social feeds during importing/etc

# MAINTENANCE_MODE = False
# MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
# MAINTENANCE_MODE_IGNORE_SUPERUSER = True
# MAINTENANCE_MODE_IGNORE_ANONYMOUS_USER = True
# MAINTENANCE_MODE_IGNORE_URLS = (r"^/users/connect/", r"^/users/OAuth2_login/")

# SILKY_AUTHENTICATION = True  # User must login
# SILKY_AUTHORISATION = True  # User must have permissions
# SILKY_PERMISSIONS = lambda user: user.is_superuser
# SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
# SILKY_INTERCEPT_PERCENT = 10

NINJA_PAGINATION_PER_PAGE = 20
OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600 * 24 * 365,
    "PKCE_REQUIRED": False,
}
OAUTH2_PROVIDER_APPLICATION_MODEL = "developer.Application"

DEVELOPER_CONSOLE_APPLICATION_CLIENT_ID = "NEODB_DEVELOPER_CONSOLE"
