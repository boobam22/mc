import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(required=True, metavar="command")
parser.set_defaults(root_path=None, version=None)
