# pyright: reportUnusedImport=false

from parser import parser

from context import context as ctx
import commands.update


def main():
    args = parser.parse_args()

    if getattr(args, "root_path", None) is not None:
        ctx.root = args.root_path
    if getattr(args, "version", None) is not None:
        ctx.version = args.version

    args.callback()


if __name__ == "__main__":
    main()
