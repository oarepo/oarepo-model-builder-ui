import json
import os
import re

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
# from tests.mock_filesystem import MockFilesystem
from io import StringIO
from pathlib import Path
from typing import Dict

from oarepo_model_builder.fs import AbstractFileSystem
import yaml

class MockFilesystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(f"File {path} not found. Known files {[f for f in self.files]}")
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def read(self, path):
        with self.open(path) as f:
            return f.read()

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret

def test_mapping():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
  "oarepo:use": "invenio",
  'settings': {
    'package': 'record_test',
  },
  'model': {
    'properties': {
      'metadata': {
        'properties': {
          'author': {
            'type': 'object',
            'properties': {
              'first_name':
              {
                'type': 'fulltext+keyword',
                'minLength':  5,
                'oarepo:ui':{
                  'default': {
                      "component": "raw",
                      "dataField": ""

                    }, 'search': {
                      "component": "raw",
                      "dataField": ""
                    }
                }
              },
              'last_name':
                      {
                'type': 'fulltext',
                'minLength':  5,
                        'oarepo:ui':{
                  'detail': {
                      "component": "raw",
                      "dataField": ""

                    }, 'search': {
                      "component": "raw",
                      "dataField": ""
                    }
                }
              }
            },
            'oarepo:ui': {
              'detail': {
                'component': 'row',
                'separator': '_',
                'items': [
                  'first_name',
                  'last_name'
                ]
              },
              'search': {
                'component': 'column',
                'items': [
                 'last_name'
                ]
              }
            }
          },
          'title': {
            'type': 'fulltext',
            'minLength': 5,
            'oarepo:sample': {
              'faker': 'name'
          },
            'oarepo:ui': {
            'detail': {
              'component': 'raw',
              'dataField': ""
            },
              'search': {
                'component': 'truncated-text',
              'dataField': "",
              'lines': 3
              }
            }
          }
        }
      }
    }
  },
  'oarepo:sample': {
    'count': 50
  },
  'oarepo:ui': {
    'detail': {
      'component': 'column',
      'items': [
        {
    "component": "icon",
    "name": "thumbs up",
    "color": "green",
    "size": "large"
  }, 'author', 'title'
      ]
    },
    'search': {
      'component': 'row',
      'items': [
            {
      "component": "icon",
    "name": "thumbs up",
    "color": "green",
    "size": "large"
              },
        'author',
        'title'
      ]
    }


  }
},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    # data = builder.filesystem.open(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json")).read()
    data = builder.filesystem.open(os.path.join("ui", "layout.yaml")).read()
    data = json.loads(data)
    expected = {
        "detail": {
            "component": "column",
            "items": [
                {
                    "component": "icon",
                    "name": "thumbs up",
                    "color": "green",
                    "size": "large"
                },
                {
                    "component": "row",
                    "separator": "_",
                    "items": [
                        {
                            "component": "raw",
                            "dataField": "author.first_name"
                        },
                        {
                            "component": "raw",
                            "dataField": "author.last_name"
                        }
                    ]
                },
                {
                    "component": "raw",
                    "dataField": "title"
                }
            ]
        },
        "search": {
            "component": "row",
            "items": [
                {
                    "component": "icon",
                    "name": "thumbs up",
                    "color": "green",
                    "size": "large"
                },
                {
                    "component": "column",
                    "items": [
                        {
                            "component": "raw",
                            "dataField": "author.last_name"
                        }
                    ]
                },
                {
                    "component": "truncated-text",
                    "dataField": "title",
                    "lines": 3
                }
            ]
        }
    }

    assert data == expected


