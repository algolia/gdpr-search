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

# Normalize webpack-stats.json produced during build (some builds emit chunk objects)
# so django-webpack-loader sees strings (avoids "expected string or bytes-like object").
try:
    import json

    stats_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'webpack-stats.json',
    )
    if os.path.exists(stats_path):
        with open(stats_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        changed = False
        if isinstance(data, dict) and 'chunks' in data and isinstance(data['chunks'], dict):
            new_chunks = {}
            for name, chunks in data['chunks'].items():
                # if chunks is a list of dicts with 'path' keys, convert to list of string paths
                if isinstance(chunks, list) and chunks and isinstance(chunks[0], dict):
                    out = []
                    for c in chunks:
                        p = c.get('path') or c.get('name')
                        if p and isinstance(p, str):
                            # prefer a web-relative bundle path when possible
                            base = os.path.basename(p)
                            if 'static' in p and 'bundles' in p:
                                out.append('/static/bundles/' + base)
                            else:
                                out.append(p)
                    new_chunks[name] = out
                    changed = True
                else:
                    new_chunks[name] = chunks

            if changed:
                data['chunks'] = new_chunks
                try:
                    with open(stats_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f)
                except Exception:
                    pass
except Exception:
    pass
