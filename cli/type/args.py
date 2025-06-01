from dataclasses import dataclass
import typing as t

if t.TYPE_CHECKING:
    from type.path import Paths


@dataclass
class BaseArgs:
    root_path: str | None
    version: str | None

    callback: t.Callable[["BaseArgs", "Paths"], None]
