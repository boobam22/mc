import shutil
from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from dataclasses import dataclass

    from types.args import BaseArgsDeprecated

    @dataclass
    class Args(BaseArgsDeprecated):
        version: str


def remove(args: "Args"):
    local_dir = args.VERSION_DIR / args.version
    assert local_dir.exists()

    shutil.rmtree(local_dir)
    args.ASSET_IDX_DIR.joinpath(f"{args.version}.json").unlink()


p = subparser.add_parser("remove", help="remove minecraft")
p.add_argument("version")
p.set_defaults(callback=remove)
