#!/bin/bash

set -e

if [ -d .venv-builder ]; then
  rm -rf .venv-builder
fi

python3 -m venv .venv-builder
.venv-builder/bin/pip install -U setuptools pip wheel

.venv-builder/bin/pip install -e .

if [ -d mock-record ]; then
    rm -rf mock-record
fi

.venv-builder/bin/oarepo-merge tests/merged_messages.po mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po
.venv-builder/bin/oarepo-compile-model tests/model.json --output-directory mock-record -vvv

# check that the messages were merged correctly
grep -q 'blah' mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po
grep -q -v 'empty' mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po

if [ -d .venv ]; then
    rm -rf .venv
fi

python3 -m venv .venv
.venv/bin/pip install -U setuptools pip wheel

source .venv/bin/activate
pip install -e 'mock-record'
pip install pytest-invenio invenio-app 'invenio-search[opensearch2]' flask-babelex oarepo-model-builder polib inflect

pytest tests
