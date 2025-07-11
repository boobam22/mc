import json
from pathlib import Path
import typing as t

from client import download_sync

if t.TYPE_CHECKING:
    from type.json_schema import VersionInfo


DEFAULT_ROOT = Path("~/.minecraft").expanduser()
VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


class Paths:
    def __init__(self):
        self._root = DEFAULT_ROOT

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root: str):
        self._root = Path(root).resolve()

    @property
    def game_root(self):
        return self.root / "game"

    @property
    def game_asset(self):
        return self.game_root / "assets"

    @property
    def game_library(self):
        return self.game_root / "libraries"

    @property
    def native(self):
        return self.game_root / "natives"

    @property
    def mod(self):
        return self.game_root / "mods"

    @property
    def metadata(self):
        return self.game_root / "metadata.json"

    @property
    def client(self):
        return self.game_root / "client.jar"

    @property
    def server(self):
        return self.game_root / "server.jar"

    @property
    def versions(self):
        return self.root / "versions"

    @property
    def manifest(self):
        return self.root / "manifest.json"

    @property
    def asset(self):
        return self.root / "assets"

    @property
    def asset_idx(self):
        return self.asset / "indexes"

    @property
    def asset_obj(self):
        return self.asset / "objects"

    @property
    def asset_static(self):
        return self.asset / "static"

    @property
    def library(self):
        return self.root / "libraries"

    @property
    def library_obj(self):
        return self.library / "objects"


class Context(Paths):
    def __init__(self):
        super().__init__()
        if self.game_root.exists():
            self._version = self.game_root.readlink().name
        else:
            self._version = None

    def update_manifest(self):
        if self.manifest.exists():
            self.manifest.unlink()
        download_sync(VERSION_MANIFEST_URL, self.manifest)

    def load_manifest(self) -> "VersionInfo":
        if not self.manifest.exists():
            self.update_manifest()
        return json.loads(self.manifest.read_text())

    def is_valid_version(self, version: str):
        for info in self.load_manifest()["versions"]:
            if info["id"] == version:
                return True
        return False

    @property
    def version(self):
        if self._version is None:
            self.version = self.load_manifest()["latest"]["release"]
            assert self._version is not None
        return self._version

    @version.setter
    def version(self, version: str):
        if self.is_valid_version(version):
            self._version = version

            if self.game_root.exists():
                self.game_root.unlink()

            real_dir = self.versions / version
            real_dir.mkdir(parents=True, exist_ok=True)
            self.game_root.symlink_to(real_dir)


context = Context()
