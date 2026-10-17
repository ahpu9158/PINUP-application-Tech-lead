"""
Problem 2: File Explorer
"""

from __future__ import annotations

import sys
from typing import Optional


class Node:
    def __init__(self, name: str, is_dir: bool, parent: Optional["Node"] = None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children: dict[str, Node] = {}


class FileExplorer:
    def __init__(self) -> None:
        self.root = Node("", is_dir=True)
        self.current = self.root

    # ---------- commands ----------
    def cwd(self) -> str:
        if self.current is self.root:
            return "/"
        parts = []
        node = self.current
        while node is not self.root:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def cd(self, path: str) -> Optional[str]:
        node = self.root if path.startswith("/") else self.current

        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if node is self.root:
                    return "currently at root."
                node = node.parent
                continue

            child = node.children.get(part)
            if child is None:
                return f"{part} not found."
            if not child.is_dir:
                return f"{path} is not a directory."
            node = child

        self.current = node
        return None

    def ls(self) -> str:
        return " ".join(sorted(self.current.children))

    def mkdir(self, name: str) -> Optional[str]:
        return self._create(name, is_dir=True)

    def touch(self, name: str) -> Optional[str]:
        return self._create(name, is_dir=False)

    # ---------- helpers ----------
    def _create(self, name: str, is_dir: bool) -> Optional[str]:
        if name in self.current.children:
            return f"{name} already exists."
        self.current.children[name] = Node(name, is_dir, parent=self.current)
        return None

    def execute(self, line: str) -> Optional[str]:
        command, _, arg = line.strip().partition(" ")
        handlers = {
            "cwd": lambda: self.cwd(),
            "cd": lambda: self.cd(arg),
            "ls": lambda: self.ls(),
            "mkdir": lambda: self.mkdir(arg),
            "touch": lambda: self.touch(arg),
        }
        handler = handlers.get(command)
        if handler is None:
            return f"{command}: command not found."
        return handler()


def main() -> None:
    explorer = FileExplorer()
    interactive = sys.stdin.isatty()

    while True:
        try:
            line = input("> " if interactive else "")
        except EOFError:
            break

        if not line.strip():
            continue
        if line.strip() == "exit":
            break

        output = explorer.execute(line)
        if output:
            print(output)


if __name__ == "__main__":
    main()
