from dataclasses import FrozenInstanceError

import pytest

from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    find_iterative,
    find_recursive,
    height_cached,
    height_iterative,
    height_recursive,
    postorder,
    preorder,
)


@pytest.fixture
def tree() -> Node:
    return Node(1, (Node(2, (Node(4), Node(5))), Node(3, (Node(6),)), Node(7)))


def test_preorder_and_dfs(tree: Node) -> None:
    expected = [1, 2, 4, 5, 3, 6, 7]
    assert list(preorder(tree)) == expected
    assert dfs_preorder_iter(tree) == expected


def test_postorder_and_bfs(tree: Node) -> None:
    assert list(postorder(tree)) == [4, 5, 2, 6, 3, 7, 1]
    assert bfs_level_order(tree) == [1, 2, 3, 7, 4, 5, 6]


@pytest.mark.parametrize("value", [1, 2, 4, 6, 7, 99])
def test_search(tree: Node, value: int) -> None:
    recursive = find_recursive(tree, value)
    assert recursive is find_iterative(tree, value)
    assert (recursive is None) == (value == 99)


def test_first_match_in_preorder() -> None:
    first, second = Node(2), Node(2)
    tree = Node(1, (first, second))
    assert find_recursive(tree, 2) is first
    assert find_iterative(tree, 2) is first


def test_empty_and_leaf() -> None:
    assert list(preorder(None)) == list(postorder(None)) == []
    assert bfs_level_order(None) == dfs_preorder_iter(None) == []
    assert find_recursive(None, 1) is find_iterative(None, 1) is None
    assert height_recursive(None) == height_iterative(None) == 0
    assert list(preorder(Node(5))) == list(postorder(Node(5))) == [5]
    assert height_recursive(Node(5)) == height_iterative(Node(5)) == 1


def test_height(tree: Node) -> None:
    height_cached.cache_clear()
    assert height_recursive(tree) == height_cached(tree) == height_iterative(tree) == 3
    height_cached.cache_clear()


def test_cache_shared_subtree_and_clear() -> None:
    shared = Node(2, (Node(3),))
    tree = Node(1, (shared, shared))
    height_cached.cache_clear()
    assert height_cached(tree) == 3
    info = height_cached.cache_info()
    assert info.hits == 1 and info.misses == 3 and info.currsize == 3
    assert height_cached(tree) == 3
    assert height_cached.cache_info().hits == 2
    height_cached.cache_clear()
    assert height_cached.cache_info().currsize == 0


def test_no_mutation(tree: Node) -> None:
    original_children = tree.children
    original = list(preorder(tree))
    list(postorder(tree))
    dfs_preorder_iter(tree)
    bfs_level_order(tree)
    find_recursive(tree, 99)
    height_recursive(tree)
    assert tree.children is original_children
    assert list(preorder(tree)) == original
    with pytest.raises(FrozenInstanceError):
        tree.value = 99  # type: ignore[misc]


def test_deep_tree_iteratively() -> None:
    tree = Node(1499)
    for value in reversed(range(1499)):
        tree = Node(value, (tree,))
    assert height_iterative(tree) == 1500
    assert dfs_preorder_iter(tree) == list(range(1500))
    assert bfs_level_order(tree) == list(range(1500))
    assert find_iterative(tree, 1499) is not None
