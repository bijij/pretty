import abc
import collections
import itertools
import linecache
import sys
import traceback
import types

from pretty import utils


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.

    Parameters
    ----------
    theme: :class:`dict`
        A theme.

    Attributes
    ----------
    theme: :class:`dict`
        A theme.
    """

    def __init__(self, *, theme=None):
        self.theme = theme or utils._default_theme

    # region public methods

    @abc.abstractmethod
    def extract_frames(self, obj, *, limit=None):
        """
        |iter|

        Extracts frames from a :data:`~types.FrameType` or
        :class:`~types.TracebackType`.

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

        Yields
        ------
        :data:`~types.FrameType`
            Frames to be formatted.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_current_exception(self, *, chain=True, limit=None):
        """
        |iter|

        Formats the current exception to be written to a file.

        This function is synonymous to :func:`traceback.format_exc`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_exception(self, type, value, traceback, *, chain=True, limit=None):
        """
        |iter|

        Formats an exception to be written to a file.

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
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_exception_only(self, type, value):
        """
        |iter|

        Formats an exception to be written to a file.

        This function is synonymous to
        :func:`traceback.format_exception_only`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_last_exception(self, *, chain=True, limit=None):
        """
        |iter|

        Formats the last exception to be written to a file.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_frames(self, frames):
        """
        |iter|

        Formats an iterable of frames to be written to a file.

        This function is synonymous to :func:`traceback.format_list`.

        Parameters
        ----------
        frames: Iterable[:data:`~types.FrameType`]
            An iterable of frames.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_stack(self, frame, *, limit=None):
        """
        |iter|

        Formats a stack to be written to a file.

        This function is synonymous to :func:`traceback.format_stack`.

        Parameters
        ----------
        frame: :data:`~types.FrameType`
            A frame.
        limit: :class:`int`
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_traceback(self, traceback, *, limit=None):
        """
        |iter|

        Formats a traceback to be written to a file.

        This function is synonymous to :func:`traceback.format_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.
        limit: :class:`int`
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    def print_current_exception(self, *, chain=True, file=None, limit=None):
        """
        Prints the current exception to a file.

        This function is synonymous to :func:`traceback.print_exc`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and print.
        """

        print("".join(self.format_current_exception(chain=chain, limit=limit)), end="", file=file or sys.stderr)

    def print_exception(self, type, value, traceback, *, chain=True, file=None, limit=None):
        """
        Prints an exception to a file.

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
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and print.
        """

        print("".join(self.format_exception(type, value, traceback, chain=chain, limit=limit)), end="", file=file or sys.stderr)

    def print_exception_only(self, type, value, *, file=None):
        """
        Prints an exception to a file.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        """

        print("".join(self.format_exception_only(type, value)), end="", file=file or sys.stderr)

    def print_last_exception(self, *, chain=True, file=None, limit=None):
        """
        Prints the last exception to a file.

        This function is synonymous to :func:`traceback.print_last`.

        Parameters
        ----------
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and print.
        """

        print("".join(self.format_last_exception(chain=chain, limit=limit)), end="", file=file or sys.stderr)

    def print_frames(self, frames, *, file=None):
        """
        Prints an iterable of frames to a file.

        This function is synonymous to ``traceback.print_list()``.

        .. NOTE: traceback.print_list, while documented in the source,
                 is not documented on docs.python.org and thus cannot
                 be linked to by intersphinx.

        Parameters
        ----------
        frames: :data:`~types.FrameType`
            An iterable of frames.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        """

        print("".join(self.format_frames(frames)), end="", file=file or sys.stderr)

    def print_stack(self, frame, *, file=None, limit=None):
        """
        Prints a stack to a file.

        This function is synonymous to :func:`traceback.print_stack`.

        Parameters
        ----------
        frame: :data:`~types.FrameType`
            A frame.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and print.
        """

        print("".join(self.format_stack(frame, limit=limit)), end="", file=file or sys.stderr)

    def print_traceback(self, traceback, *, file=None, limit=None):
        """
        Prints a traceback to a file.

        This function is synonymous to :func:`traceback.print_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.
        file
            The file to print to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and print.
        """

        print("".join(self.format_traceback(traceback, limit=limit)), end="", file=file or sys.stderr)

    def walk_stack(self, frame):
        """
        |iter|

        Walks a stack.

        This function is synonymous to :func:`traceback.walk_stack`.

        Parameters
        ----------
        frame: :data:`~types.FrameType`
            A frame.

        Yields
        ------
        :data:`~types.FrameType`
            Frames.
        """

        while frame is not None:
            yield frame

            frame = frame.f_back

    def walk_traceback(self, traceback):
        """
        |iter|

        Walks a traceback.

        This function is synonymous to :func:`traceback.walk_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.

        Yields
        ------
        :data:`~types.FrameType`
            Frames.
        """

        while traceback is not None:
            yield traceback.tb_frame

            traceback = traceback.tb_next

    # endregion
    # region private methods

    _unprintable = "<unprintable {0.__class__.__qualname__} object>"

    def _try_repr(self, value):
        try:
            return repr(value)
        except:
            return self._unprintable.format(value)

    def _try_str(self, value):
        try:
            return str(value)
        except:
            return self._unprintable.format(value)

    _sentinel = object()

    def _extract_value_traceback(self, type, value, traceback):
        if (value is self._sentinel) != (traceback is self._sentinel):
            raise ValueError("Both or neither of value and tb must be given")
        elif value is self._sentinel:
            if type is None:
                return None, None
            else:
                return type, type.__traceback__
        else:
            return value, traceback

    @utils.wrap(traceback.extract_stack)
    def _extract_stack(self, f=None, limit=None):
        return traceback.StackSummary(self.extract_frames(f or sys._getframe().f_back, limit=limit))

    @utils.wrap(traceback.extract_tb)
    def _extract_traceback(self, tb, limit=None):
        return traceback.StackSummary(self.extract_frames(tb, limit=limit))

    @utils.wrap(traceback.format_exc)
    def _format_current_exception(self, limit=None, chain=True):
        return "".join(self.format_current_exception(chain=chain, limit=limit))

    if sys.version_info >= (3, 10):
        @utils.wrap(traceback.format_exception)
        def _format_exception(self, exc, value=_sentinel, tb=_sentinel, limit=None, chain=True):
            value, tb = self._extract_value_traceback(exc, value, tb)
            return list(self.format_exception(type(value), value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, exc, value=_sentinel):
            value, _ = self._extract_value_traceback(exc, value, None)
            return list(self.format_exception_only(type(value), value))
    else:
        @utils.wrap(traceback.format_exception)
        def _format_exception(self, etype, value, tb, limit=None, chain=True):
            return list(self.format_exception(type(value), value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, etype, value):
            return list(self.format_exception_only(type(value), value))

    @utils.wrap(traceback.format_list)
    def _format_frames(self, extracted_list):
        return list(self.format_frames(extracted_list))

    @utils.wrap(traceback.format_stack)
    def _format_stack(self, f=None, limit=None):
        return list(self.format_stack(f or sys._getframe().f_back, limit=limit))

    @utils.wrap(traceback.format_tb)
    def _format_traceback(self, tb, limit=None):
        return list(self.format_traceback(tb, limit=limit))

    @utils.wrap(traceback.print_exc)
    def _print_current_exception(self, limit=None, file=None, chain=True):
        self.print_current_exception(chain=chain, file=file, limit=limit)

    if sys.version_info >= (3, 10):
        @utils.wrap(traceback.print_exception)
        def _print_exception(self, exc, value=_sentinel, tb=_sentinel, limit=None, file=None, chain=True):
            value, tb = self._extract_value_traceback(exc, value, tb)
            self.print_exception(type(value), value, tb, chain=chain, file=file, limit=limit)
    else:
        @utils.wrap(traceback.print_exception)
        def _print_exception(self, etype, value, tb, limit=None, file=None, chain=True):
            self.print_exception(type(value), value, tb, chain=chain, file=file, limit=limit)

    @utils.wrap(traceback.print_last)
    def _print_last_exception(self, limit=None, file=None, chain=True):
        self.print_last_exception(chain=chain, file=file, limit=limit)

    @utils.wrap(traceback.print_list)
    def _print_frames(self, extracted_list, file=None):
        self.print_frames(extracted_list, file=file)

    @utils.wrap(traceback.print_stack)
    def _print_stack(self, f=None, limit=None, file=None):
        self.print_stack(f or sys._getframe().f_back, file=file, limit=limit)

    @utils.wrap(traceback.print_tb)
    def _print_traceback(self, tb, limit=None, file=None):
        self.print_traceback(tb, file=file, limit=limit)

    @utils.wrap(traceback.walk_stack)
    def _walk_stack(self, f):
        f = f or sys._getframe().f_back.f_back

        for frame in self.walk_stack(f):
            yield frame, frame.f_lineno

    @utils.wrap(traceback.walk_tb)
    def _walk_traceback(self, tb):
        for frame in self.walk_traceback(tb):
            yield frame, frame.f_lineno

    # endregion


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.

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

    cause_header = traceback._cause_message
    context_header = traceback._context_message
    recursion_cutoff = traceback._RECURSIVE_CUTOFF
    traceback_header = "Traceback (most recent call last):\n"

    def extract_frames(self, obj, *, limit=None):
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

    def format_current_exception(self, *, chain=True, limit=None):
        yield from self.format_exception(*sys.exc_info(), chain=chain, limit=limit)

    def format_exception(self, type, value, traceback, *, chain=True, limit=None, seen=None):
        if chain and value is not None:
            seen = seen or set()
            seen.add(id(value))

            cause = value.__cause__

            if cause is not None and id(cause) not in seen:
                yield from self.format_exception(type(cause), cause, cause.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.cause_header

            context = value.__context__

            if context is not None and id(context) not in seen:
                yield from self.format_exception(type(context), context, context.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.context_header

        if traceback is not None:
            yield self.traceback_header
            yield from self.format_traceback(traceback, limit=limit)

        yield from self.format_exception_only(type, value)

    def format_last_exception(self, *, chain=True, limit=None):
        if not hasattr(sys, "last_type"):
            raise ValueError("no last exception")

        yield from self.format_exception(sys.last_type, sys.last_value, sys.last_traceback, chain=chain, limit=limit)

    def format_stack(self, frame, *, limit=None):
        yield from self.format_frames(self.extract_frames(frame, limit=limit))

    def format_traceback(self, traceback, *, limit=None):
        yield from self.format_frames(self.extract_frames(traceback, limit=limit))


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

    ...


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
