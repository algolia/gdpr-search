"""gdpr_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include

from macrosurl import url

from .gdpr.sitemap import GdprSitemap
from .gdpr.views import IndexView, ArticleView


sitemap_patterns = [
    url(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': {'articles': GdprSitemap()}, 'template_name': 'sitemap.html'},
        name='django.contrib.sitemaps.views.sitemap'
    )
]


i18n_urlpatterns = i18n_patterns(
    url(
        '',
        IndexView.as_view(),
        name='index'
    ),
    url(
        'gdpr-article-:id',
        ArticleView.as_view(),
        name='article'
    ),
    prefix_default_language=False
)

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + sitemap_patterns + i18n_urlpatterns
