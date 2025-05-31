import subprocess
from parser import subparser
import typing as t

if t.TYPE_CHECKING:
    from dataclasses import dataclass

    from types.args import BaseArgsDeprecated

    @dataclass
    class Args(BaseArgsDeprecated):
        args: list[str]


start_sh = """
#!/bin/sh

ROOT_DIR="${HOME}/.minecraft"

if [ -n "$2" ]; then
  exit 1
fi

if [ -n "$1" ]; then
  VERSION=$1
else
  VERSION=$(cat "${ROOT_DIR}/VERSION")
fi

WORK_DIR="${ROOT_DIR}/versions/${VERSION}"
cd ${WORK_DIR} || exit 1
echo ${VERSION} > "${ROOT_DIR}/VERSION"

java \
    -Xmx4G \
    -Djava.library.path=natives \
    -cp "$(find libraries -name '*.jar' | paste -sd:):client.jar" \
    $(cat MAINCLASS) \
    --username nia11720 \
    --version ${VERSION} \
    --gameDir ${WORK_DIR} \
    --assetsDir ${ROOT_DIR}/assets \
    --assetIndex ${VERSION} \
    --uuid 3b6de038-3d66-48cd-8816-cb3579dd2c53 \
    --accessToken 0 \
    > /dev/null  2>&1 &
"""


def start(args: "Args"):
    subprocess.run(["sh", "-c", start_sh, "script-name"] + args.args)


p = subparser.add_parser("start", help="start minecraft")
p.add_argument("args", nargs="*")
p.set_defaults(callback=start)
