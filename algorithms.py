"""Варіант 14: чисті обходи n-арного дерева та кешування висоти."""

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True, slots=True, eq=False)
class Node:
    value: int
    children: tuple["Node", ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "children", tuple(self.children))


def preorder(tree: Node | None) -> Iterator[int]:
    if tree is None:
        return
    yield tree.value
    for child in tree.children:
        yield from preorder(child)


def postorder(tree: Node | None) -> Iterator[int]:
    if tree is None:
        return
    for child in tree.children:
        yield from postorder(child)
    yield tree.value


def find_recursive(tree: Node | None, value: int) -> Node | None:
    if tree is None or tree.value == value:
        return tree
    for child in tree.children:
        found = find_recursive(child, value)
        if found is not None:
            return found
    return None


def dfs_preorder_iter(tree: Node | None) -> list[int]:
    stack, result = ([tree] if tree is not None else []), []
    while stack:
        node = stack.pop()
        result.append(node.value)
        stack.extend(reversed(node.children))
    return result


def bfs_level_order(tree: Node | None) -> list[int]:
    queue, result = deque([tree] if tree is not None else []), []
    while queue:
        node = queue.popleft()
        result.append(node.value)
        queue.extend(node.children)
    return result


def find_iterative(tree: Node | None, value: int) -> Node | None:
    stack = [tree] if tree is not None else []
    while stack:
        node = stack.pop()
        if node.value == value:
            return node
        stack.extend(reversed(node.children))
    return None


def height_recursive(tree: Node | None) -> int:
    """Висота в кількості вузлів: порожнє дерево 0, листок 1."""
    if tree is None:
        return 0
    return 1 + max((height_recursive(c) for c in tree.children), default=0)


@lru_cache(maxsize=None)
def height_cached(tree: Node | None) -> int:
    if tree is None:
        return 0
    return 1 + max((height_cached(c) for c in tree.children), default=0)


def height_iterative(tree: Node | None) -> int:
    if tree is None:
        return 0
    queue = deque([tree])
    height = 0
    while queue:
        height += 1
        for _ in range(len(queue)):
            queue.extend(queue.popleft().children)
    return height
