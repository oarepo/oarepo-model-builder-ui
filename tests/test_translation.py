from oarepo_runtime.i18n import lazy_gettext, get_locale


def test_translations_registered_cs(app):
    with app.test_request_context(headers=[("Accept-Language", "cs")]):
        print(f"{get_locale()=}")
        print("text: ", lazy_gettext("prov"))
        assert "Seznam" in lazy_gettext("prov")


def test_translations_registered_en(app):
    with app.test_request_context(headers=[("Accept-Language", "en")]):
        print(f"{get_locale()=}")
        print("text: ", lazy_gettext("lowest_price.hint"))
        assert "Enter" in lazy_gettext("lowest_price.hint")
