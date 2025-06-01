import json
import subprocess
from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from type.args import BaseArgs
    from type.path import Paths


def start(args: "BaseArgs", ctx: "Paths"):
    if (version := args.version) is None:
        version = ctx.last_version.read_text().strip()

    ctx.last_version.write_text(version)
    ctx = ctx.set_version(version)

    cwd = ctx.version_dir

    libs = [str(item.relative_to(cwd)) for item in ctx.lib_dir.glob("**/*.jar")]

    if ctx.fabric_metadata.exists():
        metadata = ctx.fabric_metadata
    else:
        metadata = ctx.metadata

    main_class: str = json.loads(metadata.read_text())["mainClass"]

    subprocess.Popen(
        [
            "java",
            "-Xmx4G",
            f"-Djava.library.path={ctx.native_dir.relative_to(cwd)}",
            "-cp",
            f"{':'.join(libs)}:{ctx.client.relative_to(cwd)}",
            main_class,
            "--version",
            version,
            "--gameDir",
            ".",
            "--assetsDir",
            str(ctx.asset_idx_dir.parent),
            "--assetIndex",
            version,
            "--username",
            "nia11720",
            "--uuid",
            "3b6de038-3d66-48cd-8816-cb3579dd2c53",
            "--accessToken",
            "0",
        ],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


p = subparser.add_parser("start", help="start minecraft")
p.add_argument("--root-path")
p.add_argument("version", nargs="?")
p.set_defaults(callback=start)
