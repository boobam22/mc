import shutil
from parser import subparser
import typing as t

from context import context as ctx


def remove(args: t.Any):
    shutil.rmtree(ctx.game_root.readlink())
    ctx.game_root.unlink()
    if (path := next(ctx.versions.glob("*"), None)) is not None:
        ctx.version = path.name


p = subparser.add_parser("remove", help="remove minecraft")
p.add_argument("--root-path")
p.add_argument("version")
p.set_defaults(callback=remove)
