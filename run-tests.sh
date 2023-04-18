#!/bin/bash

set -e

if [ -d .venv-builder ]; then
    rm -rf .venv-builder
fi

python3 -m venv .venv-builder

.venv-builder/bin/pip install -e .

if [ -d tests/mock_record ]; then
    rm -rf tests/mock_record
fi

.venv-builder/bin/oarepo-merge tests/merged_messages.po tests/mock_record/mock_record/translations/cs/LC_MESSAGES/messages.po
.venv-builder/bin/oarepo-compile-model tests/model.json --output-directory tests/mock_record -vvv

# check that the messages were merged correctly
grep -q 'blah' tests/mock_record/mock_record/translations/cs/LC_MESSAGES/messages.po
grep -q -v 'empty' tests/mock_record/mock_record/translations/cs/LC_MESSAGES/messages.po

if [ -d .venv ]; then
    rm -rf .venv
fi

python3 -m venv .venv

source .venv/bin/activate
pip install -e 'tests/mock_record'
pip install pytest-invenio invenio-app 'invenio-search[opensearch2]' flask-babelex oarepo-model-builder polib

pytest tests
