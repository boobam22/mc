import asyncio
from parser import subparser
import typing as t

from client import download

if t.TYPE_CHECKING:
    from types.args import BaseArgs

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


def update(args: "BaseArgs"):
    if args.VERSION_MANIFEST.exists():
        args.VERSION_MANIFEST.unlink()

    asyncio.run(download(VERSION_MANIFEST_URL, args.VERSION_MANIFEST))


p = subparser.add_parser("update", help="update version manifest")
p.set_defaults(callback=update)
