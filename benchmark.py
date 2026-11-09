"""Вимірювання рекурсивної, ітеративної та кешованої висоти."""

from collections.abc import Callable
from statistics import median
from timeit import repeat

from algorithms import Node, height_cached, height_iterative, height_recursive


def make_tree(depth: int, value: int = 0) -> Node:
    if depth == 0:
        return Node(value)
    return Node(value, tuple(make_tree(depth - 1, 3 * value + i + 1) for i in range(3)))


def main() -> None:
    tree = make_tree(6)
    number, repeats = 100, 5

    def cold() -> int:
        height_cached.cache_clear()
        return height_cached(tree)

    def measure(fn: Callable[[], int]) -> float:
        return median(repeat(fn, number=number, repeat=repeats)) / number * 1e6

    recursive = measure(lambda: height_recursive(tree))
    iterative = measure(lambda: height_iterative(tree))
    cached_cold = measure(cold)
    height_cached.cache_clear()
    height_cached(tree)
    cached_warm = measure(lambda: height_cached(tree))
    print("Дерево: 1093 вузли, висота 7; 5 повторів по 100 операцій")
    print(f"Рекурсія без кешу: {recursive:.2f} мкс/операцію")
    print(f"Ітеративна висота: {iterative:.2f} мкс/операцію")
    print(f"Холодний кеш (із cache_clear): {cached_cold:.2f} мкс/операцію")
    print(f"Прогрітий кеш: {cached_warm:.2f} мкс/операцію")
    print("Стан прогрітого кешу:", height_cached.cache_info())
    print("Підготовку дерева не включено; значення залежать від середовища.")
    height_cached.cache_clear()


if __name__ == "__main__":
    main()
