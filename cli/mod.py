import typing as t

from client import client, download
from context import context as ctx

if t.TYPE_CHECKING:
    from json_schema import ModrinthItem

MODRINTH = "https://api.modrinth.com"

mods = [
    "fabric-api",
    "malilib",
    "minihud",
    "litematica",
    "litematica-printer",
]


def install_mods():
    for name in mods:
        dst = ctx.mod / f"{name}.jar"
        if dst.exists():
            continue

        res = client.get(f"{MODRINTH}/v2/project/{name}/version")
        data: list["ModrinthItem"] = res.json()

        for item in data:
            if "fabric" in item["loaders"] and ctx.version in item["game_versions"]:
                jar = item["files"][0]
                download(jar["url"], dst, jar["size"])
                break
        else:
            print(f"{name} not found")
