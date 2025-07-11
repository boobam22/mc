import json
import asyncio
from parser import subparser
import typing as t

from client import download_sync, download, download_all
from context import context as ctx


ASSET_HOST = "https://resources.download.minecraft.net"


def install():
    for info in ctx.load_manifest()["versions"]:
        if info["id"] == ctx.version:
            download_sync(info["url"], ctx.metadata)
            break


p = subparser.add_parser("install", help="install minecraft")
p.add_argument("--root-path")
p.add_argument("version", nargs="?")
p.set_defaults(callback=install)
