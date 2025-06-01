from dataclasses import dataclass
from pathlib import Path
import typing as t

if t.TYPE_CHECKING:
    from types.path import Paths


@dataclass
class BaseArgsDeprecated:
    ROOT_DIR: Path
    VERSION_DIR: Path
    ASSET_IDX_DIR: Path
    ASSET_OBJ_DIR: Path
    LIB_OBJ_DIR: Path

    VERSION_MANIFEST: Path

    callback: t.Callable[["BaseArgsDeprecated"], None]


@dataclass
class BaseArgs:
    root_path: str | None
    version: str | None

    callback: t.Callable[["BaseArgs", "Paths"], None]
