from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CrawlerAPI

crawler_urls = [
    url(r'v1/crawl/$',CrawlerAPI.as_view())
]

crawler_urls = format_suffix_patterns(urlpatterns=crawler_urls)

urlpatterns = crawler_urls



