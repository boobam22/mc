import shutil
import typing as t

from client import client, download, download_all
from context import context as ctx

if t.TYPE_CHECKING:
    from client import URI
    from json_schema import FabricInfo

META_HOST = "https://meta.fabricmc.net"
MAVEN_HOST = "https://maven.fabricmc.net"


def parse_maven(maven: str):
    path, name, version = maven.split(":")
    path = path.replace(".", "/")

    return f"{path}/{name}/{version}/{name}-{version}.jar"


def install_fabric():
    if ctx.fabric_metadata.exists():
        return

    url = f"{META_HOST}/v2/versions/loader/{ctx.version}"
    data: "FabricInfo" = client.get(url).json()[0]
    url = f"{META_HOST}/v2/versions/loader/{ctx.version}/{data['loader']['version']}/profile/json"
    download(url, ctx.fabric_metadata)

    items: list["URI"] = []
    for key in ["loader", "intermediary"]:
        key = t.cast(t.Literal["loader", "intermediary"], key)
        path = parse_maven(data[key]["maven"])
        items.append((f"{MAVEN_HOST}/{path}", ctx.game_library / path, None))
    for item in data["launcherMeta"]["libraries"]["common"]:
        path = parse_maven(item["name"])
        items.append((f"{MAVEN_HOST}/{path}", ctx.game_library / path, item["size"]))

    download_all(items)

    for _, jar, _ in items:
        version = jar.parent.name
        for item in jar.parent.parent.glob("*"):
            if item.name != version:
                shutil.rmtree(item)

    ctx.main_class.write_text(data["launcherMeta"]["mainClass"]["client"])
