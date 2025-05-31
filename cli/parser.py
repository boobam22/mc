import pathlib
import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(required=True, metavar="command")

ROOT_DIR = pathlib.Path("~/.minecraft").expanduser()
parser.set_defaults(
    ROOT_DIR=ROOT_DIR,
    VERSION_MANIFEST=ROOT_DIR / "version_manifest.json",
    VERSION_DIR=ROOT_DIR / "versions",
    ASSET_IDX_DIR=ROOT_DIR / "assets" / "indexes",
    ASSET_OBJ_DIR=ROOT_DIR / "assets" / "objects",
    LIB_OBJ_DIR=ROOT_DIR / "libraries" / "objects",
)
