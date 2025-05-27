from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Optional


@dataclass
class Node:
    """
    Class representing a tree node.
    """

    key: int
    data: Any = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None


@dataclass
class BSTree:
    """
    Class representing Binary Search Tree.
    """

    root: Optional[Node] = None

    def insert(self, node: Node) -> None:
        parent = None
        current = self.root
        while current is not None:
            parent = current
            current = current.left if node.key < current.key else current.right

        if parent is None:
            self.root = node
            return

        node.parent = parent
        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

    def _transplant(self, node: Node, replacement: Optional[Node]) -> None:
        if node.parent is None:
            self.root = replacement
        else:
            if node.parent.left == node:
                node.parent.left = replacement
            else:
                node.parent.right = replacement

        if replacement is not None:
            replacement.parent = node.parent

    def _subtree_minimum(self, node: Node) -> Node:
        while node.left is not None:
            node = node.left

        return node

    def delete(self, node: Node) -> None:
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            minimum = self._subtree_minimum(node.right)

            self._transplant(minimum, minimum.right)
            self._transplant(node, minimum)
            minimum.left = node.left
            minimum.right = node.right

            if node.left is not None:
                node.left.parent = minimum

            if node.right is not None:
                node.right.parent = minimum


def inorder(node: Optional[Node]) -> None:
    if node is not None:
        inorder(node.left)
        print(node.key, end=" ")
        inorder(node.right)


def preorder(node: Optional[Node]) -> None:
    if node is not None:
        print(node.key, end=" ")
        preorder(node.left)
        preorder(node.right)


def postorder(node: Optional[Node]) -> None:
    if node is not None:
        postorder(node.left)
        postorder(node.right)
        print(node.key, end=" ")


def tree_traversal(tree: BSTree, technique: Callable[[Optional[Node]], None]) -> None:
    print(technique.__name__.capitalize() + ": ", end="")
    technique(tree.root)
    # newline
    print()


def main() -> None:
    inorder_traversal = partial(tree_traversal, technique=inorder)
    preorder_traversal = partial(tree_traversal, technique=preorder)
    postorder_traversal = partial(tree_traversal, technique=postorder)

    tree = BSTree()
    # add nodes to the tree

    inorder_traversal(tree)
    preorder_traversal(tree)
    postorder_traversal(tree)


if __name__ == "__main__":
    main()
