"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.date import (
    DateFacet,
    DateTimeFacet,
    EDTFFacet,
    EDTFIntervalFacet,
    TimeFacet,
)
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

prices = TermsFacet(field="prices", label=_("prices.label"))


expires = DateFacet(field="expires", label=_("expires.label"))


lowest_price = TermsFacet(field="lowest_price", label=_("lowest_price.label"))


tags = TermsFacet(field="tags", label=_("tags.label"))


providers_org_id = NestedLabeledFacet(
    path="providers",
    nested_facet=TermsFacet(
        field="providers.org_id", label=_("providers/org_id.label")
    ),
)


providers_name = NestedLabeledFacet(
    path="providers",
    nested_facet=TermsFacet(field="providers.name", label=_("providers/name.label")),
)


providers_area = NestedLabeledFacet(
    path="providers",
    nested_facet=TermsFacet(field="providers.area", label=_("providers/area.label")),
)


providers_tags = NestedLabeledFacet(
    path="providers",
    nested_facet=TermsFacet(field="providers.tags", label=_("providers/tags.label")),
)


en = TermsFacet(field="en", label=_("en.label"))
