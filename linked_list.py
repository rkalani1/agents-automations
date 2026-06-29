class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next  # Fix: save the next node before overwriting
        current.next = prev
        prev = current
        current = next_node
    return prev

if __name__ == '__main__':
    # Tests
    head = Node(1, Node(2, Node(3, Node(4))))

    # helper to print list
    def print_list(node):
        res = []
        while node:
            res.append(node.val)
            node = node.next
        return res

    print("Original list:", print_list(head))
    reversed_head = reverse_list(head)
    print("Reversed list:", print_list(reversed_head))

    assert print_list(reversed_head) == [4, 3, 2, 1]

    # Test empty list
    assert reverse_list(None) is None

    # Test single node
    single = Node(1)
    rev_single = reverse_list(single)
    assert print_list(rev_single) == [1]

    print("All tests passed!")
