from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Iterator
from traceback import FrameSummary
from types import FrameType, TracebackType
from typing import TextIO, TypeVar, Union


_E = TypeVar("_E", bound=BaseException)


class TracebackFormatter(metaclass=ABCMeta):
    def __init__(self, **kwargs) -> None: ...

    @abstractmethod
    def extract_frames(self, obj: Union[FrameType, TracebackType], *, limit: int=...) -> Iterator[FrameType]: ...

    @abstractmethod
    def format_current_exception(self, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    @abstractmethod
    def format_exception(self, type: type[_E], value: _E, traceback: TracebackType, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    @abstractmethod
    def format_exception_only(self, type: type[_E], value: _E) -> Iterator[str]: ...
    @abstractmethod
    def format_last_exception(self, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    @abstractmethod
    def format_frames(self, frames: Iterable[Union[FrameType, FrameSummary]]) -> Iterator[str]: ...
    @abstractmethod
    def format_stack(self, frame: FrameType, *, limit: int=...) -> Iterator[str]: ...
    @abstractmethod
    def format_traceback(self, traceback: TracebackType, *, limit: int=...) -> Iterator[str]: ...

    def print_current_exception(self, *, chain: bool=..., file: TextIO=..., limit: int=...) -> None: ...
    def print_exception(self, type: type[_E], value: _E, traceback: TracebackType, *, chain: bool=..., file: TextIO=..., limit: int=...) -> None: ...
    def print_exception_only(self, type: type[_E], value: _E, *, file: TextIO=...) -> None: ...
    def print_last_exception(self, *, chain: bool=..., file: TextIO=..., limit: int=...) -> None: ...
    def print_frames(self, frames: Iterable[Union[FrameType, FrameSummary]], *, file: TextIO=...) -> None: ...
    def print_stack(self, frame: FrameType, *, file: TextIO=..., limit: int=...) -> None: ...
    def print_traceback(self, traceback: TracebackType, *, file: TextIO=..., limit: int=...) -> None: ...

    def walk_stack(self, frame: FrameType) -> Iterator[FrameType]: ...
    def walk_traceback(self, traceback: TracebackType) -> Iterator[FrameType]: ...


class DefaultTracebackFormatter(TracebackFormatter):
    # patch for abstract method implementations
    def extract_frames(self, obj: Union[FrameType, TracebackType], *, limit: int=...) -> Iterator[FrameType]: ...
    def format_current_exception(self, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    def format_exception(self, type: type[_E], value: _E, traceback: TracebackType, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    def format_exception_only(self, type: type[_E], value: _E) -> Iterator[str]: ...
    def format_last_exception(self, *, chain: bool=..., limit: int=...) -> Iterator[str]: ...
    def format_frames(self, frames: Iterable[Union[FrameType, FrameSummary]]) -> Iterator[str]: ...
    def format_stack(self, frame: FrameType, *, limit: int=...) -> Iterator[str]: ...
    def format_traceback(self, traceback: TracebackType, *, limit: int=...) -> Iterator[str]: ...


class PrettyTracebackFormatter(DefaultTracebackFormatter):
    pass
