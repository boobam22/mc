import shutil
from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from type.args import BaseArgs
    from type.path import Paths


def remove(args: "BaseArgs", ctx: "Paths"):
    version: t.Any = {"id": args.version}
    ctx = ctx.set_version(version)

    assert ctx.version_dir.exists()
    shutil.rmtree(ctx.version_dir)
    ctx.asset_idx.unlink()


p = subparser.add_parser("remove", help="remove minecraft")
p.add_argument("--root-path")
p.add_argument("version")
p.set_defaults(callback=remove)
