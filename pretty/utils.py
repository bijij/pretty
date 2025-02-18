import sys


# NOTE: SGR color values are HSV(x°, 30%, 100%) where;
#
#       x     SGR           name
#       ---   -----------   ---------
#       0     255;179;179   red
#       30    255;217;179   orange
#       60    255;255;179   yellow
#       90    217;255;179   lime
#       120   179;255;179   green
#       150   179;255;217   turquoise
#       180   179;255;255   cyan
#       210   179;217;255   blue
#       240   179;179;255   indigo
#       270   217;179;255   purple
#       300   255;179;255   magenta
#       330   255;179;217   pink
#
#       SGR grayscale values are HSV(0°, 0%, y%) where;
#
#       y     SGR           name
#       --    -----------   -----
#       10    26;26;26      black
#       25    64;64;64      dark gray
#       50    128;128;128   middle gray
#       75    191;191;191   light gray
#       90    230;230;230   white
#
pretty_theme = {
    # colorizing abstract syntax trees
    "ast_comment_sgr": ("38;2;179;255;179", "39"),
    "ast_delimiter_sgr": ("38;2;128;128;128", "39"),
    "ast_keyword_sgr": ("38;2;179;179;255", "39"),
    "ast_name_sgr": ("38;2;191;191;191", "39"),
    "ast_operator_sgr": ("38;2;128;128;128", "39"),
    # customizing character display
    "char_cap": "\u2514",
    "char_pipe": "\u2502",
    "char_quote": "\u0022",
    # colorizing literal types
    "literal_bool_sgr": ("38;2;179;179;255", "39"),
    "literal_bytes_sgr": ("38;2;255;217;179", "39"),
    "literal_complex_sgr": ("38;2;179;255;255", "39"),
    "literal_ellipsis_sgr": ("38;2;128;128;128", "39"),
    "literal_float_sgr": ("38;2;179;255;255", "39"),
    "literal_int_sgr": ("38;2;179;255;255", "39"),
    "literal_none_sgr": ("38;2;179;179;255", "39"),
    "literal_str_sgr": ("38;2;255;217;179", "39"),
    # pretty.traceback
    "traceback_exception_sgr": ("38;2;255;179;179", "39"),
    "traceback_frame_filename_sgr": ("38;2;230;230;230", "39"),
    "traceback_frame_introspection_sgr": ("38;2;255;179;255", "39"),
    "traceback_frame_lineno_sgr": ("38;2;255;179;255", "39"),
    "traceback_frame_name_sgr": ("38;2;230;230;230", "39"),
    "traceback_frame_scope": False,
    "traceback_frame_scope_key_sgr": ("38;2;191;191;191", "39"),
    "traceback_frame_source_sgr": None,
    "traceback_header_sgr": ("38;2;230;230;230", "39"),
    "traceback_message_sgr": ("38;2;128;128;128", "39"),
}


_bool_map = {
    False: ["0", "false", "off", "disable", "no", "n"],
    True: ["1", "true", "on", "enable", "yes", "y"],
}
_bool_map = {v: k for k in _bool_map.keys() for v in _bool_map[k]}


def try_bool(obj, *, default):
    if isinstance(obj, str):
        try:
            return _bool_map[obj.lower()]
        except KeyError:
            return default
    else:
        try:
            return bool(obj)
        except Exception:
            return default


def try_name(obj, *, default):
    try:
        try:
            name = obj.__qualname__
        except AttributeError:
            name = obj.__name__
    except AttributeError:
        return default

    try:
        module = obj.__module__
    except AttributeError:
        return name

    if module not in ("__main__", "builtins"):
        module_names = module.split(".")

        i = len(module_names)
        while i:
            module_test = ".".join(module_names[:i])

            try:
                module_type = sys.modules[module_test]
            except KeyError:
                break

            obj_test = module_type
            try:
                for part in name.split("."):
                    obj_test = getattr(obj_test, part)
            except AttributeError:
                break

            if obj_test is not obj:
                break

            module = module_test

            i -= 1

        name = f"{module}.{name}"

    return name


def try_repr(obj, *, default):
    try:
        return repr(obj)
    except Exception:
        return default


def try_str(obj, *, default):
    try:
        return str(obj)
    except Exception:
        return default


def wrap(wrapped):
    def decorator(wrapper):
        def function(*args, **kwargs):
            try:
                return wrapper(*args, **kwargs)
            except Exception:
                return wrapped(*args, **kwargs)

        function.__dict__.update(wrapped.__dict__)

        function.__doc__ = wrapped.__doc__
        function.__name__ = wrapped.__name__
        function.__qualname__ = wrapped.__qualname__
        function.__module__ = wrapped.__module__
        function.__wrapped__ = wrapped

        return function

    return decorator


__all__ = [
    "try_bool",
    "try_name",
    "try_repr",
    "try_str",
    "wrap",
]
