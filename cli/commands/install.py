import json
import zipfile
import asyncio
from parser import subparser
import typing as t

from client import download, download_all
from fabric import install_fabric

if t.TYPE_CHECKING:
    from dataclasses import dataclass
    from pathlib import Path

    from client import URI
    from types.args import BaseArgsDeprecated
    from types.json_schema import Versions, VersionMeta, AssetMeta

    @dataclass
    class Args(BaseArgsDeprecated):
        version: str | None


ASSET_HOST = "https://resources.download.minecraft.net"


def parse_game(dir: "Path", meta: "VersionMeta"):
    game = meta["downloads"]

    ret: list["URI"] = []
    dst = dir / f"client.jar"
    ret.append((game["client"]["url"], dst, game["client"]["size"]))

    return ret


def parse_library(dir: "Path", meta: "VersionMeta"):
    items = meta["libraries"]

    ret: list["URI"] = []
    for item in items:
        af = item["downloads"]["artifact"]
        hash = af["sha1"]

        dst = dir / f"{hash[:2]}/{hash}"
        ret.append((af["url"], dst, af["size"]))

    return ret


def parse_asset(dir: "Path", meta: "AssetMeta"):
    items = meta["objects"]

    ret: list["URI"] = []
    for item in items.values():
        hash = item["hash"]

        url = f"{ASSET_HOST}/{hash[:2]}/{hash}"
        dst = dir / f"{hash[:2]}/{hash}"
        ret.append((url, dst, item["size"]))

    return ret


def hardlink(src: "Path", dst: "Path"):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.hardlink_to(src)


def link_library(obj_dir: "Path", local_dir: "Path", meta: "VersionMeta"):
    items = meta["libraries"]

    lib_local_dir = local_dir / "libraries"
    native_dir = local_dir / "natives"

    if lib_local_dir.exists():
        return
    lib_local_dir.mkdir()

    for item in items:
        af = item["downloads"]["artifact"]
        hash = af["sha1"]
        path = af["path"]

        src = obj_dir / f"{hash[:2]}/{hash}"
        if "-natives-" in path:
            with zipfile.ZipFile(src) as jar:
                jar.extractall(native_dir)
        else:
            hardlink(src, lib_local_dir / path)


def link_asset(obj_dir: "Path", local_dir: "Path", meta: "AssetMeta"):
    items = meta["objects"]

    asset_local_dir = local_dir / "assets"

    if asset_local_dir.exists():
        return
    asset_local_dir.mkdir()

    for path, item in items.items():
        hash = item["hash"]

        src = obj_dir / f"{hash[:2]}/{hash}"
        dst = asset_local_dir / path
        hardlink(src, dst)


async def main(args: "Args", version: "Versions.Item"):
    vid = version["id"]
    url = version["url"]
    local_dir = args.VERSION_DIR / vid
    dst = local_dir / "metadata.json"

    await download(url, dst)
    meta: "VersionMeta" = json.loads(dst.read_text())

    asset = meta["assetIndex"]
    dst = args.ASSET_IDX_DIR / f"{vid}.json"

    await download(asset["url"], dst, asset["size"])
    asset_meta: "AssetMeta" = json.loads(dst.read_text())

    items: list["URI"] = []
    items += parse_game(local_dir, meta)
    items += parse_library(args.LIB_OBJ_DIR, meta)
    items += parse_asset(args.ASSET_OBJ_DIR, asset_meta)

    await download_all(items)

    link_library(args.LIB_OBJ_DIR, local_dir, meta)
    link_asset(args.ASSET_OBJ_DIR, local_dir, asset_meta)

    main_class = local_dir / "MAINCLASS"
    main_class.write_text(meta["mainClass"])

    await install_fabric(local_dir, vid)


def install(args: "Args"):
    assert args.VERSION_MANIFEST.exists()
    versions: "Versions" = json.loads(args.VERSION_MANIFEST.read_text())

    if (vid := args.version) is None:
        vid = versions["latest"]["release"]

    for item in versions["versions"]:
        if item["id"] == vid:
            asyncio.run(main(args, item))
            break
    else:
        raise ValueError("invalid version, try to update version_manifest")


p = subparser.add_parser("install", help="install minecraft")
p.add_argument("version", nargs="?")
p.set_defaults(callback=install)
