
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import MiddlewareNotUsed
from django.db.models import Q
from leonardo.module.web.models import Page


class MultiSiteMiddleware(object):

    """activate page filter by request.get_host
    """

    actual_sites = []

    def __init__(self):
        if getattr(settings, 'MULTISITE_ENABLED', False):
            raise MiddlewareNotUsed

    def process_request(self, request):

        current = request.get_host()
        current_site = None
        # don't hit DB if is same as last
        if current not in self.actual_sites:
            try:
                current_site = Site.objects.get(
                    Q(domain=current) | Q(name__icontains=current))
            except Site.DoesNotExist:
                pass
            else:
                Page.objects.active_filters.pop('current_site', None)
                Page.objects.add_to_active_filters(Q(site=current_site),
                                                   key='current_site')
                # patch settings which is used for feincms cache keys
                settings.SITE_ID = current_site.id

            self.actual_sites = [current_site.domain
                                 if current_site else current]

            if current_site:
                self.actual_sites += current_site.name.split(';')
