from pathlib import Path

DEFAULT_ROOT = Path("~/.minecraft").expanduser()


class Context:
    _root: Path | None
    _version: str | None

    def __init__(self):
        self._root = None
        self._version = None

    @property
    def root(self):
        if self._root is None:
            return DEFAULT_ROOT
        return self._root

    @root.setter
    def root(self, root: str):
        self._root = Path(root).resolve()

    @property
    def version(self):
        if self._version is None:
            raise
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = version

        if self.game_root.exists():
            self.game_root.unlink()
        self.game_root.symlink_to(self.versions / self.version)

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


context = Context()
