from dataclasses import dataclass
from pathlib import Path
import typing as t


@dataclass
class BaseArgs:
    ROOT_DIR: Path
    VERSION_DIR: Path
    ASSET_IDX_DIR: Path
    ASSET_OBJ_DIR: Path
    LIB_OBJ_DIR: Path

    VERSION_MANIFEST: Path

    callback: t.Callable[["BaseArgs"], None]
