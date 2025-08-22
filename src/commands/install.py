import json
import shutil
import zipfile
from parser import subparser
import typing as t

from client import download, download_all
from context import context as ctx
from fabric import install_fabric

if t.TYPE_CHECKING:
    from pathlib import Path
    from client import URI
    from json_schema import Metadata, AssetInfo

ASSET_HOST = "https://resources.download.minecraft.net"


def install(args: t.Any):
    for info in ctx.load_manifest()["versions"]:
        if info["id"] == ctx.version:
            download(info["url"], ctx.metadata)
            break

    metadata: "Metadata" = json.loads(ctx.metadata.read_text())
    items: "list[URI]" = []
    links: "list[tuple[Path, Path]]" = []
    natives: "list[Path]" = []

    downloads = metadata["downloads"]
    items.append((downloads["client"]["url"], ctx.client, downloads["client"]["size"]))
    items.append((downloads["server"]["url"], ctx.server, downloads["server"]["size"]))

    liraries = metadata["libraries"]
    for item in liraries:
        af = item["downloads"]["artifact"]
        hash = af["sha1"]
        dst = ctx.library_obj / f"{hash[:2]}/{hash}"
        items.append((af["url"], dst, af["size"]))

        path = af["path"]
        if "-natives-" in path:
            natives.append(dst)
        else:
            links.append((ctx.game_library / af["path"], dst))

    asset_index = metadata["assetIndex"]
    dst = ctx.asset_idx / f"{ctx.version}.json"
    download(asset_index["url"], dst, asset_index["size"])
    asset_info: "AssetInfo" = json.loads(dst.read_text())
    for path, item in asset_info["objects"].items():
        hash = item["hash"]
        url = f"{ASSET_HOST}/{hash[:2]}/{hash}"
        dst = ctx.asset_obj / f"{hash[:2]}/{hash}"
        items.append((url, dst, item["size"]))
        links.append((ctx.game_asset / path, dst))

    download_all(items)

    for src, dst in links:
        if not src.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            src.hardlink_to(dst)
    for obj in natives:
        with zipfile.ZipFile(obj) as jar:
            jar.extractall(ctx.native)

    ctx.main_class.write_text(metadata["mainClass"])
    install_fabric()

    for src in ctx.resource.glob("**/*"):
        if src.is_file():
            relative = src.relative_to(ctx.resource)
            if relative.parts[0] == "mods":
                if len(relative.parts) == 3 and relative.parts[1] == ctx.version:
                    relative = ctx.mod / relative.parts[2]
                else:
                    continue

            dst = ctx.game_root / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)


p = subparser.add_parser("install", help="install minecraft")
p.add_argument("--root-path")
p.add_argument("version", nargs="?")
p.set_defaults(callback=install)
