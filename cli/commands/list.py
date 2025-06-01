import fnmatch
import json
from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from dataclasses import dataclass

    from type.args import BaseArgs
    from type.path import Paths
    from type.json_schema import Versions

    @dataclass
    class Args(BaseArgs):
        installed: bool
        type: t.Literal["release", "snapshot", "old_alpha", "old_beta"] | None
        parttern: str


def list(args: "Args", ctx: "Paths"):
    installed = [item.name for item in ctx.versions_dir.glob("*")]

    versions: "Versions" = json.loads(ctx.version_manifest.read_text())

    for item in versions["versions"]:
        id = item["id"]

        if args.installed and not id in installed:
            continue
        if args.type and item["type"] != args.type:
            continue
        if not fnmatch.fnmatch(id, args.parttern):
            continue

        print(id, end="")
        if not args.installed and id in installed:
            print("  [installed]")
        else:
            print()


p = subparser.add_parser("list", help="list minecraft")
p.add_argument("--root-path")
p.add_argument("--installed", action="store_true", default=False)
p.add_argument("--type", "-t", choices=["release", "snapshot", "old_alpha", "old_beta"])
p.add_argument("parttern", nargs="?", default="*")
p.set_defaults(callback=list)
