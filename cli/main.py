# pyright: reportUnusedImport=false

from parser import parser
import typing as t

import commands.update
import commands.install
import commands.remove
import commands.prune
import commands.list
import commands.start
from type.path import Paths, VersionPaths

if t.TYPE_CHECKING:
    from type.args import BaseArgs


def main():
    args = t.cast("BaseArgs", parser.parse_args())

    if args.version is None:
        ctx = Paths(args.root_path)
    else:
        ctx = VersionPaths(args.version, args.root_path)

    args.callback(args, ctx)


if __name__ == "__main__":
    main()
