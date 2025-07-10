import asyncio
from parser import subparser

from client import download
from context import context as ctx

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


def update():
    if ctx.manifest.exists():
        ctx.manifest.unlink()
    asyncio.run(download(VERSION_MANIFEST_URL, ctx.manifest))


parser = subparser.add_parser("update", help="update version manifest")
parser.add_argument("--root-path")
parser.set_defaults(callback=update)
