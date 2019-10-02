

from bitarray import bitarray
from heap import Heap

# Huffman tree implementation
class Character:

    BIT_0 = bitarray.from_number(0)
    BIT_1 = bitarray.from_number(1)

    def __init__(self, label, weight, elemental=False):
        self.weight = weight
        self._label = label
        self.left = None
        self.right = None

        # A character is elemental when it can't be decomposed into any more
        # characters
        self.elemental = elemental

    def __getitem__(self, bit):
        if bit == 0:
            return self.left
        if bit == 1:
            return self.right
        raise Exception('Invalid item {}, valid items are 0 or 1'.format(bit))

    @property
    def label(self):
        if self.elemental:
            return self._label[0]
        return self._label

    @classmethod
    def build_tree(cls, character_list):
        character_heap = Heap()
        for character in character_list:
            character_heap.insert(character)
        while character_heap.size() > 1:
            min_a, min_b = character_heap.pop(), character_heap.pop()
            new_label = list(min_a.label)
            new_label.extend(min_b.label)
            new_weight = min_a.weight + min_b.weight
            character_tree = cls(new_label, new_weight)
            character_tree.left = min_a
            character_tree.right = min_b
            character_heap.insert(character_tree)

        # the first character of our heap is the new tree
        return character_heap.pop()

    def decode_next(self, bit_array, index=0):
        bit = bit_array[index]
        subtree = self[bit]
        if subtree.elemental:
            return subtree.label, index + 1
        return subtree.decode_next(bit_array, index=index + 1)

    def decode(self, bit_array):
        decoded, index = "", 0
        while index < len(bit_array):
            c, index = self.decode_next(bit_array, index)
            decoded += c
        return decoded

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __ne__(self, other):
        return self.weight != other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight >= other.weight

    def direction(self, c):
        if c in self.left.label:
            return 0
        elif c in self.right.label:
            return 1
        else:
            raise Exception

    def code(self, c):
        if c not in self.label:
            raise Exception
        if self.elemental:
            return bitarray()
        bit = self.direction(c)

        return bitarray.from_number(bit) + self[bit].code(c)

    def __repr__(self):
        cadena = 'Character(' + self.label + ',' + str(self.weight) + ')'
        return cadena
