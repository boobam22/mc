from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    root_dir: Path

    version_manifest: Path
    last_version: Path

    asset_idx_dir: Path
    asset_obj_dir: Path

    lib_obj_dir: Path

    versions_dir: Path

    def __init__(self, root: str | None = None):
        if root is None:
            root_dir = Path("~/.minecraft").expanduser()
        else:
            root_dir = Path(root).resolve()

        object.__setattr__(self, "root_dir", root_dir)

        object.__setattr__(self, "version_manifest", root_dir / "version-manifest.json")
        object.__setattr__(self, "last_version", root_dir / "LAST_VERSION")

        object.__setattr__(self, "asset_idx_dir", root_dir / "assets" / "indexes")
        object.__setattr__(self, "asset_obj_dir", root_dir / "assets" / "objects")

        object.__setattr__(self, "lib_obj_dir", root_dir / "libraries" / "objects")

        object.__setattr__(self, "versions_dir", root_dir / "versions")

    def set_version(self, version: str):
        return VersionPaths(version, str(self.root_dir))


@dataclass(frozen=True)
class VersionPaths(Paths):
    version_dir: Path

    asset_idx: Path
    client: Path

    asset_dir: Path
    lib_dir: Path
    native_dir: Path

    mod_dir: Path

    metadata: Path
    fabric_metadata: Path

    def __init__(self, version: str, root: str | None = None):
        super().__init__(root)

        version_dir = self.versions_dir / version

        object.__setattr__(self, "version_dir", version_dir)

        object.__setattr__(self, "asset_idx", self.asset_idx_dir / f"{version}.json")
        object.__setattr__(self, "client", self.version_dir / "client.jar")

        object.__setattr__(self, "asset_dir", version_dir / "assets")
        object.__setattr__(self, "lib_dir", version_dir / "libraries")
        object.__setattr__(self, "native_dir", version_dir / "natives")

        object.__setattr__(self, "mod_dir", version_dir / "mods")

        object.__setattr__(self, "metadata", version_dir / "metadata.json")
        object.__setattr__(
            self, "fabric_metadata", version_dir / "fabric-metadata.json"
        )
