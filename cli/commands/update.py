from parser import subparser

from context import context as ctx


parser = subparser.add_parser("update", help="update version manifest")
parser.add_argument("--root-path")
parser.set_defaults(callback=ctx.update_manifest)
