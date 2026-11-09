"""Обов'язкова база ЛР4: quicksort, бінарне дерево та Fibonacci."""

from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import lru_cache
from random import Random


def quicksort(values: Sequence[int], *, seed: int = 14) -> list[int]:
    """Власний RNG із заданим seed: глобальний random-стан не змінюється."""
    rng = Random(seed)

    def sort(part: Sequence[int]) -> list[int]:
        if len(part) <= 1:
            return list(part)
        pivot = rng.choice(part)
        left = [x for x in part if x < pivot]
        middle = [x for x in part if x == pivot]
        right = [x for x in part if x > pivot]
        return sort(left) + middle + sort(right)

    return sort(values)


@dataclass(frozen=True, slots=True)
class BinaryNode:
    key: int
    left: "BinaryNode | None" = None
    right: "BinaryNode | None" = None


def preorder(tree: BinaryNode | None) -> Iterator[int]:
    if tree is None:
        return
    yield tree.key
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def inorder(tree: BinaryNode | None) -> Iterator[int]:
    if tree is None:
        return
    yield from inorder(tree.left)
    yield tree.key
    yield from inorder(tree.right)


def postorder(tree: BinaryNode | None) -> Iterator[int]:
    if tree is None:
        return
    yield from postorder(tree.left)
    yield from postorder(tree.right)
    yield tree.key


def bfs_level_order(tree: BinaryNode | None) -> list[int]:
    queue, result = deque([tree] if tree is not None else []), []
    while queue:
        node = queue.popleft()
        result.append(node.key)
        queue.extend(child for child in (node.left, node.right) if child is not None)
    return result


def dfs_preorder_iter(tree: BinaryNode | None) -> list[int]:
    stack, result = ([tree] if tree is not None else []), []
    while stack:
        node = stack.pop()
        result.append(node.key)
        stack.extend(child for child in (node.right, node.left) if child is not None)
    return result


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n має бути невід'ємним")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n має бути невід'ємним")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
