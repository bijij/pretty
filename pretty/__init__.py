from __future__ import annotations

import sys
from typing import NamedTuple

from pretty import traceback, utils

__all__ = []


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


def main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    all = utils.environment_to_boolean("PYTHONPRETTY", None)

    if all is False:
        return

    theme = utils.environment_to_theme("PYTHONPRETTYTHEME", None)

    if all is True or utils.environment_to_boolean("PYTHONPRETTYTRACEBACK", False):
        try:
            traceback.hook(theme=theme)
        except BaseException as e:
            if hasattr(sys, "last_value"):
                print("ERROR:pretty:failed to hook pretty.traceback")
            else:
                print("ERROR:pretty:failed to hook pretty.traceback, see traceback.print_last()")
                sys.last_type, sys.last_value, sys.last_traceback = type(e), e, e.__traceback__
