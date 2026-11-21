"""hello-forge 命令行入口：python -m hello_forge"""

import argparse

from .core import hello


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hello-forge",
        description="输入一句话需求，输出一份可直接推送的仓库骨架。",
    )
    parser.add_argument("name", nargs="?", default="world", help="问候对象")
    args = parser.parse_args()
    print(hello(args.name))


if __name__ == "__main__":
    main()
