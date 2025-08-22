import subprocess
from parser import subparser
import typing as t

from context import context as ctx


def start(args: t.Any):
    cwd = ctx.game_root
    libs = [str(item.relative_to(cwd)) for item in ctx.game_library.glob("**/*.jar")]

    subprocess.Popen(
        [
            "java",
            "-Xmx4G",
            f"-Djava.library.path={ctx.native.relative_to(cwd)}",
            "-cp",
            f"{':'.join(libs)}:{ctx.client.relative_to(cwd)}",
            ctx.main_class.read_text().strip(),
            "--version",
            ctx.version,
            "--assetsDir",
            str(ctx.game_asset),
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
