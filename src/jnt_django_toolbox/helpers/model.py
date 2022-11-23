def ensure_fields_saved(save_kwargs, fields):
    """Ensuring fields saving (extending "update_fields")."""
    update_fields = save_kwargs.get("update_fields")
    if not update_fields:
        return

    save_kwargs["update_fields"] = tuple(set(list(update_fields) + fields))
