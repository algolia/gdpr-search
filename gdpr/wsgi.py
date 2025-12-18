"""
WSGI config for gdpr_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gdpr.settings.prod")

# Monkey-patch webpack_loader to handle dict-format chunks from webpack-bundle-tracker
try:
    import json
    from webpack_loader import loaders
    
    _original_get_assets = loaders.WebpackLoader.get_assets
    
    def _patched_get_assets(self):
        """Normalize webpack-stats chunks to handle both dict and string formats"""
        assets = _original_get_assets(self)
        
        # Normalize chunks: convert dicts to strings and build assets mapping
        if isinstance(assets, dict) and "chunks" in assets:
            chunks = assets.get("chunks", {})
            if isinstance(chunks, dict):
                normalized_chunks = {}
                assets_map = {}
                
                for name, chunk_list in chunks.items():
                    if isinstance(chunk_list, list) and chunk_list:
                        # Convert dict entries to path strings
                        if isinstance(chunk_list[0], dict):
                            paths = []
                            for item in chunk_list:
                                path = item.get("path") or item.get("name", "")
                                if path:
                                    # Use web-relative path
                                    base = path.split("/")[-1]
                                    web_path = "/static/bundles/" + base
                                    paths.append(web_path)
                                    # Build assets entry keyed by path
                                    assets_map[web_path] = [{"name": base, "path": web_path}]
                            normalized_chunks[name] = paths
                        else:
                            normalized_chunks[name] = chunk_list
                            # Build assets for string paths too
                            for p in chunk_list:
                                if isinstance(p, str):
                                    assets_map[p] = [{"name": p.split("/")[-1], "path": p}]
                
                if normalized_chunks:
                    assets["chunks"] = normalized_chunks
                if assets_map:
                    if "assets" not in assets:
                        assets["assets"] = {}
                    assets["assets"]["assets"] = assets_map
        
        return assets
    
    loaders.WebpackLoader.get_assets = _patched_get_assets
except Exception:
    pass

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
