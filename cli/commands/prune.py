from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from types.args import BaseArgs
    from types.path import Paths


def prune(args: "BaseArgs", ctx: "Paths"):
    for dir in [ctx.lib_obj_dir, ctx.asset_obj_dir]:
        for obj in list(dir.glob("**/*")):
            if obj.is_file() and obj.stat().st_nlink == 1:
                obj.unlink()


p = subparser.add_parser("prune", help="prune objects")
p.set_defaults(callback=prune)
