from __future__ import absolute_import

from constance import config
from allowedsites import CachedAllowedSites


class CachedAllowedSites(CachedAllowedSites):

    '''Support for aliases:
        site.domain = 'main-site.com'
        site.name = 'site.com;site1.com;www.site.com'

    '''

    def get_domains(self):
        """
        Yields domains *without* any ports defined, as that's what
        `validate_host` wants
        """
        from django.http.request import split_domain_port
        raw_sites = self.get_raw_sites()
        domains = set()
        raw_domains = []
        for site in raw_sites:
            raw_domains += [site.domain]
            if config.MULTISITE_ALIASES:
                raw_domains += site.name.split(';')
        for domain in raw_domains:
            domain_host, domain_port = split_domain_port(domain)
            domains.add(domain_host)
        return frozenset(domains)
