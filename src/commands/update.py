from parser import subparser
import typing as t

from context import context as ctx


def update(args: t.Any):
    ctx.update_manifest()


parser = subparser.add_parser("update", help="update version manifest")
parser.add_argument("--root-path")
parser.set_defaults(callback=update)
