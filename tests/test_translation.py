from oarepo_runtime.i18n import lazy_gettext, get_locale
from flask import g


def clear_babel_context():
    # for invenio 12
    try:
        from flask_babel import SimpleNamespace
    except ImportError:
        return
    g._flask_babel = SimpleNamespace()



def test_translations_registered_cs(app):
    clear_babel_context()
    with app.test_request_context(headers=[("Accept-Language", "cs")]):
        print(f"{get_locale()=}")
        print("text: ", lazy_gettext("prov"))
        assert "Seznam" in lazy_gettext("prov")


def test_translations_registered_en(app):
    clear_babel_context()
    with app.test_request_context(headers=[("Accept-Language", "en")]):
        print(f"{get_locale()=}")
        print("text: ", lazy_gettext("lowest_price.hint"))
        assert "Enter" in lazy_gettext("lowest_price.hint")
