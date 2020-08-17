def ensure_fields_saved(save_kwargs, fields):
    if "update_fields" not in save_kwargs:
        return

    save_kwargs["update_fields"] = tuple(
        set(list(save_kwargs["update_fields"]) + fields),
    )
