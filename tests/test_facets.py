import os
import json

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

import pytest
DUMMY_YAML = "test.yaml"


@pytest.mark.xfail
def test_facets(app):
    schema = load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "record": {
                "use": "invenio",
                "properties": {
                    "b": {
                        "type": "object",
                        "properties": {
                            "c": {
                                "type": "keyword",
                            },
                            "d": {"type": "fulltext+keyword"},
                            "f": {
                                "type": "object",
                                "properties": {"g": {"type": "keyword"}},
                            },
                            "e": "fulltext",
                        },
                    }
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    ui_json = builder.filesystem.open(os.path.join("test", "models", "ui.json")).read()
    assert ui_json is not None

    ui_spec = json.loads(ui_json)
    print(ui_spec)
    assert ui_spec["children"]["b"]["children"]["c"]["facet"] == "b_c"
