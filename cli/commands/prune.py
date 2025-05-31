from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from types.args import BaseArgsDeprecated


def prune(args: "BaseArgsDeprecated"):
    for dir in [args.LIB_OBJ_DIR, args.ASSET_OBJ_DIR]:
        for obj in list(dir.glob("**/*")):
            if obj.is_file() and obj.stat().st_nlink == 1:
                obj.unlink()


p = subparser.add_parser("prune", help="prune objects")
p.set_defaults(callback=prune)
