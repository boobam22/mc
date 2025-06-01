# pyright: reportUnusedImport=false

from parser import parser
import typing as t

import commands.update
import commands.install
import commands.remove
import commands.prune
import commands.list
import commands.start
from type.path import Paths

if t.TYPE_CHECKING:
    from type.args import BaseArgs


def main():
    args = t.cast("BaseArgs", parser.parse_args())

    ctx = Paths(args.root_path)

    args.callback(args, ctx)


if __name__ == "__main__":
    main()
