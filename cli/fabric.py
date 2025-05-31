import shutil
import typing as t

from client import client, download_all

if t.TYPE_CHECKING:
    from pathlib import Path

    from types.json_schema import FabricMeta
    from client import URI

META_HOST = "https://meta.fabricmc.net"
MAVEN_HOST = "https://maven.fabricmc.net"


def parse_maven(maven: str):
    path, name, version = maven.split(":")
    path = path.replace(".", "/")

    return f"{path}/{name}/{version}/{name}-{version}.jar"


async def install_fabric(local_dir: "Path", version: str):
    metadata = local_dir / "fabric-metadata.json"

    if metadata.exists():
        return

    url = f"{META_HOST}/v2/versions/loader/{version}"
    res = await client.get(url)
    data: "FabricMeta" = res.json()[0]

    lib_local_dir = local_dir / "libraries"

    url = f"{META_HOST}/v2/versions/loader/{version}/{data['loader']['version']}/profile/json"
    items: list["URI"] = [(url, metadata, None)]

    for key in ["loader", "intermediary"]:
        key = t.cast(t.Literal["loader", "intermediary"], key)
        path = parse_maven(data[key]["maven"])
        items.append((f"{MAVEN_HOST}/{path}", lib_local_dir / path, None))

    for item in data["launcherMeta"]["libraries"]["common"]:
        path = parse_maven(item["name"])
        items.append((f"{MAVEN_HOST}/{path}", lib_local_dir / path, item["size"]))

    await download_all(items)

    for _, jar, _ in items:
        version = jar.parent.name
        for item in jar.parent.parent.iterdir():
            if item.name != version:
                shutil.rmtree(item)

    main_class = local_dir / "MAINCLASS"
    main_class.write_text(data["launcherMeta"]["mainClass"]["client"])
