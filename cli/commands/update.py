import asyncio
from parser import subparser
import typing as t

from client import download

if t.TYPE_CHECKING:
    from type.args import BaseArgs
    from type.path import Paths

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


def update(args: "BaseArgs", ctx: "Paths"):
    if ctx.version_manifest.exists():
        ctx.version_manifest.unlink()

    asyncio.run(download(VERSION_MANIFEST_URL, ctx.version_manifest))


p = subparser.add_parser("update", help="update version manifest")
p.add_argument("--root-path")
p.set_defaults(callback=update)
