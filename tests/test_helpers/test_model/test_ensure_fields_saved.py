from jnt_django_toolbox.helpers.model import ensure_fields_saved


def test_ensure_fields_save():
    kwargs = {"update_fields": ["created"]}

    ensure_fields_saved(kwargs, ["title"])

    assert set(kwargs["update_fields"]) == {"created", "title"}


def test_ensure_fields_save_empty():
    kwargs = {}

    ensure_fields_saved(kwargs, ["title"])

    assert not kwargs
