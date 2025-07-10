# pyright: reportUnusedImport=false

from parser import parser

import commands.update


def main():
    args = parser.parse_args()
    args.callback()


if __name__ == "__main__":
    main()
