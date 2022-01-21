from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, NoReturn, TextIO, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from types import FrameType, TracebackType
    from traceback import FrameSummary, StackSummary

import abc
import collections
import itertools
import linecache
import sys
import traceback
import types

from pretty import utils


class _Sentinel:
    ...


BE = TypeVar("BE", bound=BaseException)


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.
    """

    __slots__ = ()

    def __init__(self, **kwargs: Any) -> None:
        pass

    @abc.abstractmethod
    def extract_frames(self, obj: FrameType | TracebackType | None, *, limit: int = None) -> Iterator[FrameType]:
        """
        |iter|

        Extracts frames from a :data:`frame <types.FrameType>` or
        :class:`traceback <types.TracebackType>`.

        This function is synonymous to both
        :func:`traceback.extract_stack` and
        :func:`traceback.extract_tb`.

        Parameters
        ----------
        obj: Union[:data:`~types.FrameType`, \
                   :class:`~types.TracebackType`]
            A frame or traceback.
        limit: :class:`int`
            The maximum number of frames to extract.


        :yields: :data:`~types.FrameType`
        """
        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_current_exception(self, *, chain: bool = True, limit: int = None, **kwargs: Any) -> Iterator[str]:
        """
        |iter|

        Formats the current exception.

        This function is synonymous to :func:`traceback.format_exc`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        **kwargs
            Additional keyword arguments are optional.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_exception(self, type: type[BE] | None, value: BE | None, traceback: TracebackType | None, *, chain: bool = True, limit: int = None, **kwargs: Any) -> Iterator[str]:
        """
        |iter|

        Formats an exception.

        This function is synonymous to
        :func:`traceback.format_exception`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        **kwargs
            Additional keyword arguments are optional.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_exception_only(self, type: type[BE] | None, value: BE | None, **kwargs: Any) -> Iterator[str]:
        """
        |iter|

        Formats an exception line.

        This function is synonymous to
        :func:`traceback.format_exception_only`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        **kwargs
            Keyword arguments are optional.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_last_exception(self, *, chain: bool = True, limit: int = None, **kwargs: Any) -> Iterator[str]:
        """
        |iter|

        Formats the last exception.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        **kwargs
            Additional keyword arguments are optional.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_frames(self, frames: Iterable[FrameSummary | FrameType], **kwargs: Any) -> Iterator[str]:
        """
        |iter|

        Formats an iterable of frames.

        This function is synonymous to :func:`traceback.format_list`.

        Parameters
        ----------
        frames: Iterable[Union[:class:`~traceback.FrameSummary`, \
                               :data:`~types.FrameType`]]
            An iterable of frames.
        **kwargs
            Keyword arguments are optional.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def get_current_exception(self) -> tuple[type[BE] | None, BE | None, TracebackType | None]:
        """
        Gets the current exception.

        Returns
        -------
        Tuple[Optional[Type[:exc:`BaseException`]], \
              Optional[:exc:`BaseException`], \
              Optional[:data:`~types.TracebackType`]]
            A (type, value, traceback) tuple.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_last_exception(self) -> tuple[type[BE] | None, BE | None, TracebackType | None]:
        """
        Gets the last exception.

        Returns
        -------
        Tuple[Optional[Type[:exc:`BaseException`]], \
              Optional[:exc:`BaseException`], \
              Optional[:data:`~types.TracebackType`]]
            A (type, value, traceback) tuple.
        """

        raise NotImplementedError

    def print_current_exception(self, *, chain: bool = True, file: TextIO = None, limit: int = None) -> None:
        """
        Prints the current exception to :data:`~sys.stderr`.

        This function is synonymous to :func:`traceback.print_exc`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file: :func:`TextIO <open>`
            The file to print to. Defaults to :data:`~sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        self.write_current_exception(chain=chain, file=file or sys.stderr, limit=limit)

    def print_exception(self, type: type[BE] | None, value: BE | None, traceback: TracebackType | None, *, chain: bool = True, file: TextIO = None, limit: int = None) -> None:
        """
        Prints an exception to :data:`~sys.stderr`.

        This function is synonymous to
        :func:`traceback.print_exception`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file: :func:`TextIO <open>`
            The file to print to. Defaults to :data:`~sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        self.write_exception(type, value, traceback, chain=chain, file=file or sys.stderr, limit=limit)

    def print_exception_only(self, type: type[BE] | None, value: BE | None, *, file: TextIO = None) -> None:
        """
        Prints an exception to :data:`~sys.stderr`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        file: :func:`TextIO <open>`
            The file to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_exception_only(type, value, file=file or sys.stderr)

    def print_last_exception(self, *, chain: bool = True, file: TextIO = None, limit: int = None) -> None:
        """
        Prints the last exception to :data:`~sys.stderr`.

        This function is synonymous to :func:`traceback.print_last`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file: :func:`TextIO <open>`
            The file to print to. Defaults to :data:`~sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        self.write_last_exception(chain=chain, file=file or sys.stderr, limit=limit)

    def print_frames(self, frames: Iterable[FrameSummary | FrameType], *, file: TextIO = None) -> None:
        """
        Prints an iterable of frames to :data:`~sys.stderr`.

        This function is synonymous to ``traceback.print_list()``.

        .. NOTE: traceback.print_list, while documented in the source,
                 is not documented on docs.python.org and thus cannot
                 be linked to by intersphinx.

        Parameters
        ----------
        frames: Iterable[Union[:class:`~traceback.FrameSummary`, \
                               :data:`~types.FrameType`]]
            An iterable of frames.
        file: :func:`TextIO <open>`
            The file to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_frames(frames, file=file or sys.stderr)

    @abc.abstractmethod
    def walk_stack(self, frame: FrameType | None) -> Iterator[FrameType]:
        """
        |iter|

        Walks a stack.

        This function is synonymous to :func:`traceback.walk_stack`.

        Parameters
        ----------
        frame: :data:`~types.FrameType`
            A frame.


        :yields: :data:`~types.FrameType`
        """
        raise NotImplementedError

        yield

    @abc.abstractmethod
    def walk_traceback(self, traceback: TracebackType | None) -> Iterator[FrameType]:
        """
        |iter|

        Walks a traceback.

        This function is synonymous to :func:`traceback.walk_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.


        :yields: :data:`~types.FrameType`
        """

        raise NotImplementedError

        yield

    def write_current_exception(self, *, file: TextIO, chain: bool = True, limit: int = None) -> None:
        """
        Writes the current exception to a file.

        Parameters
        ----------
        file: :func:`TextIO <open>`
            The file to write to.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        try:
            tty = file.isatty()
        except AttributeError:
            tty = False

        file.write("".join(self.format_current_exception(chain=chain, limit=limit, tty=tty)))

    def write_exception(self, type: type[BE] | None, value: BE | None, traceback: TracebackType | None, *, file: TextIO, chain: bool = True, limit: int = None) -> None:
        """
        Writes an exception to a file.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        file: :func:`TextIO <open>`
            The file to write to.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        try:
            tty = file.isatty()
        except AttributeError:
            tty = False

        file.write("".join(self.format_exception(type, value, traceback, chain=chain, limit=limit, tty=tty)))

    def write_exception_only(self, type: type[BE] | None, value: BE | None, *, file: TextIO) -> None:
        """
        Writes an exception to a file.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        file: :func:`TextIO <open>`
            The file to write to.
        """

        try:
            tty = file.isatty()
        except AttributeError:
            tty = False

        file.write("".join(self.format_exception_only(type, value, tty=tty)))

    def write_last_exception(self, *, file: TextIO, chain: bool = True, limit: int = None) -> None:
        """
        Writes the last exception to a file.

        Parameters
        ----------
        file: :func:`TextIO <open>`
            The file to write to.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        try:
            tty = file.isatty()
        except AttributeError:
            tty = False

        file.write("".join(self.format_last_exception(chain=chain, limit=limit, tty=tty)))

    def write_frames(self, frames: Iterable[FrameSummary | FrameType], *, file: TextIO) -> None:
        """
        Writes an iterable of frames to a file.

        Parameters
        ----------
        frames: Iterable[Union[:class:`~traceback.FrameSummary`, \
                               :data:`~types.FrameType`]]
            An iterable of frames.
        file: :func:`TextIO <open>`
            The file to write to.
        """

        try:
            tty = file.isatty()
        except AttributeError:
            tty = False

        file.write("".join(self.format_frames(frames, tty=tty)))

    def _try_name(self, type: Any) -> str:
        try:
            name = type.__name__
        except AttributeError:
            name = self._try_unprintable(type)
        else:
            module = type.__module__

            if module not in ("__main__", "builtins"):
                name = f"{module}.{name}"
        finally:
            return name  # type: ignore

    def _try_repr(self, value: Any) -> str:
        try:
            value = repr(value)
        except:
            value = self._try_unprintable(value)
        finally:
            return value

    def _try_str(self, value: Any) -> str:
        try:
            value = str(value)
        except:
            value = self._try_unprintable(value)
        finally:
            return value

    _unprintable: ClassVar[str] = "<unprintable object>"
    _unprintable_fmt: ClassVar[str] = "<unprintable {0.__class__.__qualname__} object>"

    def _try_unprintable(self, value: Any) -> str:
        try:
            value = self._unprintable_fmt.format(value)
        except:
            value = self._unprintable
        finally:
            return value

    _sentinel = _Sentinel()

    @overload
    def _extract_value_traceback(self, type: Any, value: _Sentinel, traceback: TracebackType | None) -> NoReturn:
        ...

    @overload
    def _extract_value_traceback(self, type: Any, value: BaseException | None, traceback: _Sentinel) -> NoReturn:
        ...

    @overload
    def _extract_value_traceback(self, type: None, value: _Sentinel, traceback: _Sentinel) -> tuple[None, None]:
        ...

    @overload
    def _extract_value_traceback(self, type: BE, value: _Sentinel, traceback: _Sentinel) -> tuple[BE, TracebackType | None]:
        ...

    @overload
    def _extract_value_traceback(self, type: type[BE] | None, value: BE | None, traceback: TracebackType | None) -> tuple[BE, TracebackType | None]:
        ...

    @overload
    def _extract_value_traceback(self, type: type[BE] | BE | None, value: BE | None | _Sentinel, traceback: TracebackType | None | _Sentinel) -> tuple[None, None] | tuple[BE, TracebackType | None] | NoReturn:
        ...

    def _extract_value_traceback(self, type: type[BE] | BE | None, value: BE | None | _Sentinel, traceback: TracebackType | None | _Sentinel) -> tuple[None, None] | tuple[BE, TracebackType | None] | NoReturn:
        if isinstance(value, _Sentinel) != isinstance(traceback, _Sentinel):
            raise ValueError("Both or neither of value and tb must be given")
        elif isinstance(value, _Sentinel):
            if type is None:
                return None, None
            else:
                return type, type.__traceback__  # type: ignore
        else:
            return value, traceback  # type: ignore

    @utils.wrap(traceback.extract_stack)
    def _extract_stack(self, f: FrameType = None, limit: int = None) -> StackSummary:
        frames = self.extract_frames(f or sys._getframe().f_back, limit=limit)
        return traceback.StackSummary(frames)  # type: ignore

    @utils.wrap(traceback.extract_tb)
    def _extract_traceback(self, tb: TracebackType, limit: int = None) -> StackSummary:
        frames = self.extract_frames(tb, limit=limit)
        return traceback.StackSummary(frames)  # type: ignore

    @utils.wrap(traceback.format_exc)
    def _format_current_exception(self, limit=None, chain=True):
        return "".join(self.format_current_exception(chain=chain, limit=limit))

    if sys.version_info >= (3, 10):

        @utils.wrap(traceback.format_exception)
        def _format_exception(self, exc: type[BE] | BE | None, value: BE | None | _Sentinel = _sentinel, tb: TracebackType | None | _Sentinel = _sentinel, limit: int = None, chain: bool = True) -> list[str]:
            _value, _tb = self._extract_value_traceback(exc, value, tb)
            return list(self.format_exception(type(_value), _value, _tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, exc: type[BE] | BE | None, value: BE | None | _Sentinel = _sentinel) -> list[str]:
            _value, _ = self._extract_value_traceback(exc, value, None)
            return list(self.format_exception_only(type(_value), _value))

    else:

        @utils.wrap(traceback.format_exception)
        def _format_exception(self, etype: type[BE], value: BE, tb: TracebackType, limit: int = None, chain: bool = True) -> list[str]:
            return list(self.format_exception(type(value), value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, etype: type[BE], value: BE) -> list[str]:
            return list(self.format_exception_only(type(value), value))

    @utils.wrap(traceback.format_list)
    def _format_frames(self, extracted_list: list[FrameSummary]) -> list[str]:
        return list(self.format_frames(extracted_list))

    @utils.wrap(traceback.format_stack)
    def _format_stack(self, f: FrameType = None, limit: int = None) -> list[str]:
        return list(self.format_frames(self.extract_frames(f or sys._getframe().f_back, limit=limit)))

    @utils.wrap(traceback.format_tb)
    def _format_traceback(self, tb: TracebackType, limit: int = None) -> list[str]:
        return list(self.format_frames(self.extract_frames(tb, limit=limit)))

    @utils.wrap(traceback.print_exc)
    def _print_current_exception(self, limit: int = None, file: TextIO = None, chain: bool = True) -> None:
        self.print_current_exception(chain=chain, file=file, limit=limit)

    if sys.version_info >= (3, 10):

        @utils.wrap(traceback.print_exception)
        def _print_exception(self, exc: type[BE] | BE | None, value: BE | _Sentinel = _sentinel, tb: TracebackType | _Sentinel = _sentinel, limit: int = None, file: TextIO = None, chain: bool = True) -> None:
            _value, _tb = self._extract_value_traceback(exc, value, tb)
            self.print_exception(type(_value), _value, _tb, chain=chain, file=file, limit=limit)

    else:

        @utils.wrap(traceback.print_exception)
        def _print_exception(self, etype, value, tb, limit=None, file=None, chain=True):
            self.print_exception(type(value), value, tb, chain=chain, file=file, limit=limit)

    @utils.wrap(traceback.print_last)
    def _print_last_exception(self, limit: int = None, file: TextIO = None, chain: bool = True) -> None:
        self.print_last_exception(chain=chain, file=file, limit=limit)

    @utils.wrap(traceback.print_list)
    def _print_frames(self, extracted_list: list[FrameSummary], file: TextIO = None) -> None:
        self.print_frames(extracted_list, file=file)

    @utils.wrap(traceback.print_stack)
    def _print_stack(self, f: FrameType = None, limit: int = None, file: TextIO = None) -> None:
        self.print_frames(self.extract_frames(f or sys._getframe().f_back, limit=limit), file=file)

    @utils.wrap(traceback.print_tb)
    def _print_traceback(self, tb: TracebackType, limit: int = None, file: TextIO = None) -> None:
        self.print_frames(self.extract_frames(tb, limit=limit), file=file)

    @utils.wrap(traceback.walk_stack)
    def _walk_stack(self, f: FrameType | None) -> Iterator[tuple[FrameType, int | None]]:
        f = f or sys._getframe().f_back
        if f is not None:
            f = f.f_back

        for frame in self.walk_stack(f):
            yield frame, frame.f_lineno

    @utils.wrap(traceback.walk_tb)
    def _walk_traceback(self, tb: TracebackType) -> Iterator[tuple[FrameType, int | None]]:
        for frame in self.walk_traceback(tb):
            yield frame, frame.f_lineno


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.

    Attributes
    ----------
    cause_header: :class:`str`
        The message yielded after an exception's cause.
    context_header: :class:`str`
        The message yielded after an exception's context.
    recursion_cutoff: :class:`int`
        The number of the same frame to display before instead
        displaying a recursion message.
    traceback_header: :class:`str`
        The message yielded before an exception's traceback.
    """

    __slots__ = ()

    cause_header: ClassVar[str] = traceback._cause_message  # type: ignore
    context_header: ClassVar[str] = traceback._context_message  # type: ignore
    recursion_cutoff: ClassVar[int] = traceback._RECURSIVE_CUTOFF  # type: ignore
    traceback_header: ClassVar[str] = "Traceback (most recent call last):\n"

    def extract_frames(self, obj: FrameType | TracebackType, *, limit: int = None) -> Iterator[FrameType]:
        if isinstance(obj, types.FrameType):
            generator = reversed(list(self.walk_stack(obj)))
        elif isinstance(obj, types.TracebackType):
            generator = self.walk_traceback(obj)
        else:
            generator = obj

        limit = limit or getattr(sys, "tracebacklimit", None)
        if limit is not None:
            if limit >= 0:
                generator = itertools.islice(generator, limit)
            else:
                generator = collections.deque(generator, -limit)

        for frame in generator:
            if isinstance(frame, tuple):
                frame, _ = frame

            linecache.lazycache(frame.f_code.co_filename, frame.f_globals)

            yield frame

    def format_current_exception(self, *, chain: bool = True, limit: int = None, **kwargs: Any) -> Iterator[str]:
        yield from self.format_exception(*self.get_current_exception(), chain=chain, limit=limit)

    def format_exception(self, type: type[BE] | None, value: BE | None, traceback: TracebackType | None, *, chain: bool = True, limit: int = None, seen: set[int] = None, **kwargs: Any) -> Iterator[str]:
        if chain and value is not None:
            seen = seen or set()
            seen.add(id(value))

            cause = value.__cause__

            if cause is not None and id(cause) not in seen:
                yield from self.format_exception(cause.__class__, cause, cause.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.cause_header

            context = value.__context__
            context_suppressed = value.__suppress_context__

            if cause is None and context is not None and not context_suppressed and id(context) not in seen:
                yield from self.format_exception(context.__class__, context, context.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.context_header

        if traceback is not None:
            yield self.traceback_header
            yield from self.format_frames(self.extract_frames(traceback), limit=limit)

        yield from self.format_exception_only(type, value)

    def format_exception_line(self, type: type[BE], value: BE, **kwargs: Any) -> Iterator[str]:
        type_name = self._try_name(type)
        value_str = self._try_str(value)

        if value is None or not value_str:
            line = f"{type_name}\n"
        else:
            line = f"{type_name}: {value_str}\n"

        yield line

    def format_last_exception(self, *, chain: bool = True, limit: int = None, **kwargs: Any) -> Iterator[str]:
        yield from self.format_exception(*self.get_last_exception(), chain=chain, limit=limit)

    def get_current_exception(self) -> tuple[type[BaseException] | None, BaseException | None, TracebackType | None]:
        return sys.exc_info()

    def get_last_exception(self) -> tuple[type[BaseException] | None, BaseException | None, TracebackType | None]:
        if not hasattr(sys, "last_type"):
            raise ValueError("no last exception")

        return (sys.last_type, sys.last_value, sys.last_traceback)

    def walk_stack(self, frame: FrameType | None) -> Iterator[FrameType]:
        while frame is not None:
            yield frame

            frame = frame.f_back

    def walk_traceback(self, traceback: TracebackType | None) -> Iterator[FrameType]:
        while traceback is not None:
            yield traceback.tb_frame

            traceback = traceback.tb_next


class PrettyTracebackFormatter(DefaultTracebackFormatter):
    """
    A pretty :class:`.TracebackFormatter`.

    Parameters
    ----------
    theme: :class:`dict`
        A theme.

    Attributes
    ----------
    cause_header: :class:`str`
        The message yielded after an exception's cause.
    context_header: :class:`str`
        The message yielded after an exception's context.
    recursion_cutoff: :class:`int`
        The number of the same frame to display before instead
        displaying a recursion message.
    theme: :class:`dict`
        A theme.
    traceback_header: :class:`str`
        The message yielded before an exception's traceback.
    """

    __slots__ = ("theme",)

    def __init__(self, *, theme: dict[str, Any] = None, **kwargs: Any) -> None:
        self.theme: dict[str, Any] = theme or utils.pretty_theme
        super().__init__(**kwargs)


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
