from flask_babelex import lazy_gettext as _
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class MockRecordSearchOptions(InvenioSearchOptions):
    """MockRecordRecord search options."""

    facets = {
        "prices": facets.prices,
        "expires": facets.expires,
        "lowest_price": facets.lowest_price,
        "tags": facets.tags,
        "providers_org_id": facets.providers_org_id,
        "providers_name": facets.providers_name,
        "providers_area": facets.providers_area,
        "providers_tags": facets.providers_tags,
        "en": facets.en,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }
