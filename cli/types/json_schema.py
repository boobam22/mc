# pyright: reportGeneralTypeIssues=false

import typing as t


class Versions(t.TypedDict):
    class Latest(t.TypedDict):
        release: str
        snapshot: str

    latest: Latest

    class Item(t.TypedDict):
        id: str
        type: t.Literal["release", "snapshot", "old_alpha", "old_beta"]
        url: str
        time: str
        releaseTime: str

    versions: list[Item]


class VersionMeta(t.TypedDict):
    class AssetIndex(t.TypedDict):
        id: str
        sha1: str
        size: int
        totalSize: int
        url: str

    assetIndex: AssetIndex

    class Downloads(t.TypedDict):
        class Uri(t.TypedDict):
            sha1: str
            size: int
            url: str

        client: Uri
        server: Uri

    downloads: Downloads

    class Library(t.TypedDict):
        class Downloads(t.TypedDict):
            class Artifact(t.TypedDict):
                path: str
                sha1: str
                size: int
                url: str

            artifact: Artifact

        downloads: Downloads

    libraries: list[Library]
    mainClass: str


class AssetMeta(t.TypedDict):
    class Asset(t.TypedDict):
        hash: str
        size: int

    objects: dict[str, Asset]


class FabricMeta(t.TypedDict):
    class Maven(t.TypedDict):
        maven: str
        version: str

    intermediary: Maven
    loader: Maven

    class LauncherMeta(t.TypedDict):
        class Libraries(t.TypedDict):
            class Item(t.TypedDict):
                name: str
                sha1: str
                url: str
                size: int

            common: list[Item]

        libraries: Libraries

        class MainClass(t.TypedDict):
            client: str
            server: str

        mainClass: MainClass

    launcherMeta: LauncherMeta
