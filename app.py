"""I/O-демонстрація обходів, кешу та базових алгоритмів."""

import sys

from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    find_recursive,
    height_cached,
    height_iterative,
    height_recursive,
    postorder,
    preorder,
)
from basics import fib, fib_iter, quicksort


def main() -> None:
    tree = Node(1, (Node(2, (Node(4), Node(5))), Node(3, (Node(6),)), Node(7)))
    print("=== N-АРНЕ ДЕРЕВО | ВАРІАНТ 14 ===")
    print("Preorder:", list(preorder(tree)))
    print("Postorder:", list(postorder(tree)))
    print("DFS:", dfs_preorder_iter(tree))
    print("BFS:", bfs_level_order(tree))
    found = find_recursive(tree, 6)
    print("Пошук 6:", found.value if found is not None else None)
    print("Пошук 99:", find_recursive(tree, 99))
    print("Висота (рекурсія / цикл):", height_recursive(tree), height_iterative(tree))
    shared = Node(8, (Node(9), Node(10)))
    dag = Node(0, (shared, shared))
    height_cached.cache_clear()
    print("Висота зі спільним піддеревом:", height_cached(dag))
    print("Кеш після першого виклику:", height_cached.cache_info())
    height_cached(dag)
    print("Кеш після повторного виклику:", height_cached.cache_info())
    height_cached.cache_clear()
    print("Кеш після очищення:", height_cached.cache_info())
    print("Quicksort:", quicksort([3, 1, 2, 2]))
    print("Fibonacci(20), рекурсія / цикл:", fib(20), fib_iter(20))
    fib.cache_clear()
    print("Ліміт рекурсії:", sys.getrecursionlimit())


if __name__ == "__main__":
    main()
