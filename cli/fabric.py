import shutil
import typing as t

from client import client, download, download_all

if t.TYPE_CHECKING:
    from client import URI
    from type.path import VersionPaths
    from type.json_schema import FabricMeta

META_HOST = "https://meta.fabricmc.net"
MAVEN_HOST = "https://maven.fabricmc.net"


def parse_maven(maven: str):
    path, name, version = maven.split(":")
    path = path.replace(".", "/")

    return f"{path}/{name}/{version}/{name}-{version}.jar"


async def install_fabric(ctx: "VersionPaths"):
    if ctx.fabric_metadata.exists():
        return

    version = ctx.version_dir.name

    url = f"{META_HOST}/v2/versions/loader/{version}"
    res = await client.get(url)
    data: "FabricMeta" = res.json()[0]

    url = f"{META_HOST}/v2/versions/loader/{version}/{data['loader']['version']}/profile/json"
    await download(url, ctx.fabric_metadata)

    items: list["URI"] = []

    for key in ["loader", "intermediary"]:
        key = t.cast(t.Literal["loader", "intermediary"], key)
        path = parse_maven(data[key]["maven"])
        items.append((f"{MAVEN_HOST}/{path}", ctx.lib_dir / path, None))

    for item in data["launcherMeta"]["libraries"]["common"]:
        path = parse_maven(item["name"])
        items.append((f"{MAVEN_HOST}/{path}", ctx.lib_dir / path, item["size"]))

    await download_all(items)

    for _, jar, _ in items:
        version = jar.parent.name
        for item in jar.parent.parent.iterdir():
            if item.name != version:
                shutil.rmtree(item)
