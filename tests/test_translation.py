from flask_babelex import gettext
from flask_babelex import get_locale


def test_translations_registered(app):
    with app.test_request_context(headers=[("Accept-Language", "cs")]):
        print(f"{get_locale()=}")
        print("text: ", gettext("prov"))
        assert "Seznam" in gettext("prov")
    with app.test_request_context(headers=[("Accept-Language", "en")]):
        print(f"{get_locale()=}")
        print("text: ", gettext("lowest_price.hint"))
        assert "Enter" in gettext("lowest_price.hint")
