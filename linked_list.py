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
