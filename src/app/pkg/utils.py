import os


def get_int_from_env(name_var: str, default: int) -> int:
    var = int(str(os.environ.get(name_var)))
    return var if isinstance(var, int) else default
