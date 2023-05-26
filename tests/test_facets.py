import json

import importlib_resources


def test_facets(app):
    ref = importlib_resources.files('mock_record.models').joinpath('ui.json')
    data = json.loads(ref.read_text())
    assert data['children']['en']['facet'] == 'en'
    assert data['children']['prices']['child']['facet'] == 'prices'
    assert data['children']['providers']['child']['children']['area']['facet'] == 'providers_area'
