from parser import subparser
import zipfile
import shutil
import typing as t

from client import download
from context import context as ctx

RESOURCE_URL = "https://github.com/boobam22/chest/archive/refs/heads/main.zip"


def update(args: t.Any):
    ctx.update_manifest()

    shutil.rmtree(ctx.resource)
    tmp = ctx.resource / "tmp.zip"
    download(RESOURCE_URL, tmp)

    with zipfile.ZipFile(tmp) as zip:
        for member in zip.namelist():
            if member.startswith("chest-main/mc") and not member.endswith("/"):
                dst = ctx.resource / member[14:]
                with zip.open(member) as src:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(src.read())
    tmp.unlink()


parser = subparser.add_parser("update", help="update version manifest")
parser.add_argument("--root-path")
parser.set_defaults(callback=update)
