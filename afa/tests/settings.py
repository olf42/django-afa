USE_TZ = False
SECRET_KEY = "fake_key_for_testing"
INSTALLED_APPS = [
    "afa",
    "afa.tests",
]
DATABASES = dict(
    default=dict(
        ENGINE="django.db.backends.sqlite3",
        NAME=":memory:",
    )
)
