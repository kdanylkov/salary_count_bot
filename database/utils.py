from sqlalchemy import inspect


def object_as_dict(obj):
    excluded_fields = ["id", "user_id"]
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
        if c not in excluded_fields
    }
