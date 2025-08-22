# pyright: reportUnusedImport=false

from parser import parser

from context import context as ctx
import commands.update
import commands.install
import commands.list
import commands.remove
import commands.prune
import commands.start


def main():
    args = parser.parse_args()

    if getattr(args, "root_path", None) is not None:
        ctx.root = args.root_path
    if getattr(args, "version", None) is not None:
        ctx.version = args.version

    args.callback(args)


if __name__ == "__main__":
    main()
