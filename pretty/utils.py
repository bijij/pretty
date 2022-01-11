import functools
import os
import re


_env_all = "PYTHONPRETTY"
_env_theme = "PYTHONPRETTYTHEME"
_env_traceback = "PYTHONPRETTYTRACEBACK"


_bool_map = {
    False: ["false", "0", "no", "n", "disable", "off"],
    True: ["true", "1", "yes", "y", "enable", "on"],
}


def environment_to_bool(name, default):
    try:
        value = os.environ[name]
    except KeyError:
        return default
    else:
        value = value.lower()

        for (boolean, values) in _bool_map.items():
            if value in values:
                return boolean

        return default


pretty_theme = {
    "ast_braces_sgr": "38;2;179;179;179",
    "ast_brackets_sgr": "38;2;179;179;179",
    "ast_comment_sgr": "38;2;179;255;179",
    "ast_keyword_sgr": "38;2;179;179;255",
    "ast_operator_sgr": "38;2;179;179;255",
    "ast_parenthesis_sgr": "38;2;179;179;179",

    "char_cap": "\u2514",
    "char_pipe": "\u2502",
    "char_quote": "\"",

    "introspection_sgr": "38;2;255;179;255",

    "traceback_exception_sgr": "38;2;255;179;179",

    "type_bool_sgr": "38;2;179;179;255",
    "type_bytes_sgr": "38;2;255;217;179",
    "type_complex_sgr": "38;2;179;255;255",
    "type_float_sgr": "38;2;179;255;255",
    "type_int_sgr": "38;2;179;255;255",
    "type_none_sgr": "38;2;179;179;255",
    "type_str_sgr": "38;2;255;217;179",
}


def environment_to_theme(name, default):
    try:
        value = os.environ[name]
    except KeyError:
        return default
    else:
        values = value.split("|")

        theme = _default_theme.copy()

        for value in values:
            try:
                name, value = value.split("=")
            except ValueError:
                pass
            else:
                name = name.lower().strip()
                value = value.strip()

                def _repl(match):
                    return chr(int(match.group(0)[2:], 16))

                value = re.sub(r"u\+[0-9]{4}|U\+[0-9]{8}", _repl, value)

                theme[name] = value

        return theme


def wrap(wrapped):
    def decorator(wrapper):
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__name__ = wrapped.__name__
        wrapper.__qualname__ = wrapped.__qualname__

        return wrapper

    return decorator


__all__ = [
    "environment_to_bool",
    "environment_to_theme",
    "wrap",
]
