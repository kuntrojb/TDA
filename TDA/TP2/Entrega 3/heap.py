

# Simple min heap implementation
class Heap:
    def __init__(self):
        self.elements = []

    def pop(self):

        if self.size() == 1:
            return self.elements.pop()

        top, leaf = self.elements[0], self.elements.pop()
        self.elements[0] = leaf
        index = 0
        balanced = False

        while not balanced:
            left, left_index = self.left_child(index, return_index=True)
            right, right_index = self.right_child(index, return_index=True)

            # if the original leaf is now actually a leaf, we are done
            if left is None:
                balanced = True
                break

            group = filter(lambda x: x is not None, [leaf, right, left])
            min_element = min(group)

            # TODO: reduce the if-else clauses
            if leaf == min_element:
                balanced = True
                break
            elif left == min_element:
                self.elements[index] = left
                self.elements[left_index] = leaf
                index = left_index
            elif right == min_element:
                self.elements[index] = right
                self.elements[right_index] = leaf
                index = right_index

        return top

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

    def __getitem__(self, index, return_index=False):
        val = None
        if index < self.size():
            val = self.elements[index]
        if return_index:
                return val, index
        return val

    def left_child(self, index, return_index=False):
        return self.__getitem__(2 * index + 1, return_index)

    def right_child(self, index, return_index=False):
        return self.__getitem__(2 * index + 2, return_index)

    def parent_index(self, index):
        return (index - 1) // 2
