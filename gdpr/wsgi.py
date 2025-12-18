"""
WSGI config for gdpr_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gdpr.settings.prod")


# Make whitenoise import compatible with older and newer versions.
try:
    # whitenoise 4+ exposes WhiteNoise at top-level
    from whitenoise import WhiteNoise

    class DjangoCompressorWhiteNoise(WhiteNoise):
        def __init__(self, app):
            super(DjangoCompressorWhiteNoise, self).__init__(app)

        def is_immutable_file(self, path, url):
            from django.conf import settings

            try:
                is_immutable = super(
                    DjangoCompressorWhiteNoise, self
                ).is_immutable_file(path, url)
            except Exception:
                is_immutable = False
            if (
                not is_immutable
                and getattr(settings, "COMPRESS_OUTPUT_DIR", None) in url
            ):
                return True
            return is_immutable

except Exception:
    # Fallback for older whitenoise versions that provide DjangoWhiteNoise
    from whitenoise.django import DjangoWhiteNoise as _DjangoWhiteNoise

    class DjangoCompressorWhiteNoise(_DjangoWhiteNoise):
        def is_immutable_file(self, path, url):
            is_immutable = super(DjangoCompressorWhiteNoise, self).is_immutable_file(
                path, url
            )
            if not is_immutable:
                from django.conf import settings

                if getattr(settings, "COMPRESS_OUTPUT_DIR", None) in url:
                    return True
            return is_immutable


application = DjangoCompressorWhiteNoise(get_wsgi_application())
