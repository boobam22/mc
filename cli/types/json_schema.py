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
