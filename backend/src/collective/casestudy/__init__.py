"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "2.0.0a4"

PACKAGE_NAME = "collective.casestudy"


_ = MessageFactory(PACKAGE_NAME)

#: Domain holding the country names, synced from pycountry's own catalogs by
#: ``python -m collective.casestudy.locales`` rather than extracted from code.
COUNTRIES_DOMAIN = f"{PACKAGE_NAME}.countries"

_country = MessageFactory(COUNTRIES_DOMAIN)

logger = logging.getLogger(PACKAGE_NAME)
