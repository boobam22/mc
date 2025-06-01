import typing as t

from client import client, download

if t.TYPE_CHECKING:
    from type.path import VersionPaths
    from type.json_schema import ModrinthItem

MODRINTH = "https://api.modrinth.com"

mods = [
    "fabric-api",
    # carpet
    "carpet",
    "gca",
    "carpet-tis-addition",
    # masa
    "malilib",
    "minihud",
    "tweakeroo",
    "litematica",
    "litematica-printer",
    "item-scroller",
    # map
    "xaeros-minimap",
    "xaeros-world-map",
    # jade
    "jade",
    # worldedit
    "worldedit",
]


async def download_mods(ctx: "VersionPaths"):
    version = ctx.version_dir.name

    for mod in mods:
        dst = ctx.mod_dir / f"{mod}-{version}.jar"
        if dst.exists():
            continue

        res = await client.get(f"{MODRINTH}/v2/project/{mod}/version")
        data: list["ModrinthItem"] = res.json()

        for item in data:
            if version in item["game_versions"]:
                jar = item["files"][0]
                await download(jar["url"], dst, jar["size"])
                break
        else:
            print(f"{mod}:{version} not found")
