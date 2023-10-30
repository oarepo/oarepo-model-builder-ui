#!/bin/bash

set -e

OAREPO_VERSION=${OAREPO_VERSION:-11}
OAREPO_VERSION_MAX=$((OAREPO_VERSION+1))

BUILDER_VENV=".venv-builder"
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .


if [ -d mock-record ]; then
    rm -rf mock-record
fi

$BUILDER_VENV/bin/oarepo-merge tests/merged_messages.po mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po
$BUILDER_VENV/bin/oarepo-compile-model tests/model.json --output-directory mock-record -vvv

# check that the messages were merged correctly
grep -q 'blah' mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po
grep -q -v 'empty' mock-record/mock_record/translations/cs/LC_MESSAGES/messages.po

VENV_TESTS=".venv-tests"

if test -d $VENV_TESTS ; then
	rm -rf $VENV_TESTS
fi

python3 -m venv $VENV_TESTS
. $VENV_TESTS/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install pytest-invenio

pip install -e 'mock-record'

pytest tests
