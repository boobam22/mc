# pyright: reportUnusedImport=false

from parser import parser
import typing as t

import commands.update
import commands.install
import commands.remove
import commands.prune
import commands.list
import commands.start

if t.TYPE_CHECKING:
    from types.args import BaseArgs


def main():
    args = t.cast("BaseArgs", parser.parse_args())
    args.callback(args)


if __name__ == "__main__":
    main()
