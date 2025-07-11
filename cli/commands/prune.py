from parser import subparser
import typing as t

from context import context as ctx


def prune(args: t.Any):
    for dir in [ctx.library_obj, ctx.asset_obj]:
        for obj in list(dir.glob("**/*")):
            if obj.is_file() and obj.stat().st_nlink == 1:
                obj.unlink()


p = subparser.add_parser("prune", help="prune objects")
p.add_argument("--root-path")
p.set_defaults(callback=prune)
