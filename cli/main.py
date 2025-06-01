# pyright: reportUnusedImport=false

import json
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
    from type.json_schema import Versions


def main():
    args = t.cast("BaseArgs", parser.parse_args())

    ctx = Paths(args.root_path)

    if args.callback.__name__ != "update":
        assert ctx.version_manifest.exists()
        versions: "Versions" = json.loads(ctx.version_manifest.read_text())

        if (version := args.version) is None:
            version = versions["latest"]["release"]

        for item in versions["versions"]:
            if item["id"] == version:
                ctx.set_version(item)
                break
        else:
            raise

    args.callback(args, ctx)


if __name__ == "__main__":
    main()
