from random import Random

import pytest

from basics import (
    BinaryNode,
    bfs_level_order,
    dfs_preorder_iter,
    fib,
    fib_iter,
    inorder,
    postorder,
    preorder,
    quicksort,
)


@pytest.mark.parametrize("values", [[], [1], [3, 2, 1], [2, 2, 1, 3, 2], [-1, 0, -3]])
def test_quicksort(values: list[int]) -> None:
    original = list(values)
    assert quicksort(values) == sorted(values)
    assert values == original


def test_quicksort_random_and_reproducible_seed() -> None:
    rng = Random(14)
    values = [rng.randrange(-100, 101) for _ in range(1000)]
    assert quicksort(values, seed=14) == sorted(values)
    assert quicksort(values, seed=42) == sorted(values)


def test_binary_traversals() -> None:
    tree = BinaryNode(
        4,
        BinaryNode(2, BinaryNode(1), BinaryNode(3)),
        BinaryNode(6, None, BinaryNode(7)),
    )
    assert list(preorder(tree)) == dfs_preorder_iter(tree) == [4, 2, 1, 3, 6, 7]
    assert list(inorder(tree)) == [1, 2, 3, 4, 6, 7]
    assert list(postorder(tree)) == [1, 3, 2, 7, 6, 4]
    assert bfs_level_order(tree) == [4, 2, 6, 1, 3, 7]
    assert list(inorder(None)) == bfs_level_order(None) == []


def test_fibonacci_values_and_cache() -> None:
    fib.cache_clear()
    assert [fib(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert all(fib(n) == fib_iter(n) for n in range(100))
    before = fib.cache_info().hits
    fib(99)
    assert fib.cache_info().hits == before + 1
    fib.cache_clear()
    assert fib.cache_info().currsize == 0


def test_fibonacci_negative() -> None:
    with pytest.raises(ValueError):
        fib(-1)
    with pytest.raises(ValueError):
        fib_iter(-1)
