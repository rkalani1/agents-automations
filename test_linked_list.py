import pytest
from linked_list import Node, reverse_list

def to_list(node):
    """Helper to convert linked list to python list for easy comparison"""
    res = []
    while node:
        res.append(node.val)
        node = node.next
    return res

def test_reverse_list_multiple_nodes():
    head = Node(1, Node(2, Node(3, Node(4))))
    reversed_head = reverse_list(head)
    assert to_list(reversed_head) == [4, 3, 2, 1]

def test_reverse_list_empty():
    assert reverse_list(None) is None

def test_reverse_list_single_node():
    single = Node(1)
    rev_single = reverse_list(single)
    assert to_list(rev_single) == [1]
