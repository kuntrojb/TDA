

# Simple min heap implementation
class Heap:
    def __init__(self):
        self.elements = []

    def pop(self):
        if self.size() == 1:
            return self.elements.pop()
        element = self.elements[0]
        self.elements[0] = self.elements.pop()
        index = 0
        balanced = False

        leaf = self.elements[0]

        while not balanced:
            left_index = self.left_child_index(index)
            right_index = self.right_child_index(index)
            if left_index >= len(self.elements):
                balanced = True
                break
            left = self.elements[left_index]

            # TODO: reduce the if-else clauses
            if right_index < len(self.elements):
                right = self.elements[right_index]
                if leaf == min(left, right, leaf):
                    balanced = True
                elif left == min(left, right, leaf):
                    self.elements[index] = left
                    self.elements[left_index] = leaf
                    index = left_index
                elif right == min(left, right, leaf):
                    self.elements[index] = right
                    self.elements[right_index] = leaf
                    index = right_index
            else:
                if leaf == min(left, leaf):
                    balanced = True
                elif left == min(left, leaf):
                    self.elements[index] = left
                    self.elements[left_index] = leaf
                    index = left_index
        return element

    def insert(self, element):
        self.elements.append(element)
        index = len(self.elements) - 1
        balanced = False
        while not balanced:
            parent_index = self.parent_index(index)
            parent = self.elements[parent_index]
            if element < parent:
                self.elements[index] = parent
                self.elements[parent_index] = element
                index = parent_index
            else:
                balanced = True

    def size(self):
        return len(self.elements)

    def left_child_index(self, index):
        return 2 * index + 1

    def right_child_index(self, index):
        return 2 * index + 2

    def parent_index(self, index):
        return (index - 1) // 2
