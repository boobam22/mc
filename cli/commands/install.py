import json
import zipfile
import asyncio
from parser import subparser
import typing as t

from client import download, download_all
from fabric import install_fabric

if t.TYPE_CHECKING:
    from pathlib import Path

    from client import URI
    from type.args import BaseArgs
    from type.path import Paths, VersionPaths
    from type.json_schema import Versions, VersionMeta, AssetMeta


ASSET_HOST = "https://resources.download.minecraft.net"


def parse_game(meta: "VersionMeta", ctx: "VersionPaths"):
    ret: list["URI"] = []

    client = meta["downloads"]["client"]
    ret.append((client["url"], ctx.client, client["size"]))

    return ret


def parse_library(meta: "VersionMeta", ctx: "VersionPaths"):
    ret: list["URI"] = []

    for item in meta["libraries"]:
        af = item["downloads"]["artifact"]
        hash = af["sha1"]

        dst = ctx.lib_obj_dir / f"{hash[:2]}/{hash}"
        ret.append((af["url"], dst, af["size"]))

    return ret


def parse_asset(meta: "AssetMeta", ctx: "VersionPaths"):
    ret: list["URI"] = []

    for item in meta["objects"].values():
        hash = item["hash"]

        url = f"{ASSET_HOST}/{hash[:2]}/{hash}"
        dst = ctx.asset_obj_dir / f"{hash[:2]}/{hash}"
        ret.append((url, dst, item["size"]))

    return ret


def hardlink(src: "Path", dst: "Path"):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.hardlink_to(src)


def link_library(meta: "VersionMeta", ctx: "VersionPaths"):
    if ctx.native_dir.exists():
        return

    for item in meta["libraries"]:
        af = item["downloads"]["artifact"]
        hash = af["sha1"]
        path = af["path"]

        src = ctx.lib_obj_dir / f"{hash[:2]}/{hash}"
        if "-natives-" in path:
            with zipfile.ZipFile(src) as jar:
                jar.extractall(ctx.native_dir)
        else:
            hardlink(src, ctx.lib_dir / path)


def link_asset(meta: "AssetMeta", ctx: "VersionPaths"):
    if ctx.asset_dir.exists():
        return

    for path, item in meta["objects"].items():
        hash = item["hash"]

        src = ctx.asset_obj_dir / f"{hash[:2]}/{hash}"
        dst = ctx.asset_dir / path
        hardlink(src, dst)


async def main(url: str, ctx: "VersionPaths"):
    await download(url, ctx.metadata)
    meta: "VersionMeta" = json.loads(ctx.metadata.read_text())

    asset = meta["assetIndex"]
    await download(asset["url"], ctx.asset_idx, asset["size"])
    asset_meta: "AssetMeta" = json.loads(ctx.asset_idx.read_text())

    items: list["URI"] = []
    items += parse_game(meta, ctx)
    items += parse_library(meta, ctx)
    items += parse_asset(asset_meta, ctx)

    await download_all(items)

    link_library(meta, ctx)
    link_asset(asset_meta, ctx)

    await install_fabric(ctx)


def install(args: "BaseArgs", ctx: "Paths"):
    assert ctx.version_manifest.exists()
    versions: "Versions" = json.loads(ctx.version_manifest.read_text())

    if (version := args.version) is None:
        version = versions["latest"]["release"]

    for item in versions["versions"]:
        if item["id"] == version:
            asyncio.run(main(item["url"], ctx.set_version(version)))
            break
    else:
        raise


p = subparser.add_parser("install", help="install minecraft")
p.add_argument("--root-path")
p.add_argument("version", nargs="?")
p.set_defaults(callback=install)
