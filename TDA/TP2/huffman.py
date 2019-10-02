

from bitarray import bitarray
from heap import Heap
from math import ceil

# Huffman tree implementation
class Character:

    BIT_0 = bitarray.from_number(0)
    BIT_1 = bitarray.from_number(1)
    EMPTY = bitarray()

    def __init__(self, label, weight, elemental=False):
        self.weight = weight
        if isinstance(label, set):
            self._label = label
        else:
            self._label = {label}
        self.left = None
        self.right = None

        # A character is elemental when it can't be decomposed into any more
        # characters
        self.elemental = elemental
        if self.elemental:
            if isinstance(label, bytearray) or isinstance(label, str):
                self.value = label
            elif isinstance(label, int):
                byte_length = ceil(label.bit_length()/8)
                self.value = label.to_bytes(length=byte_length, byteorder='big')
            else:
                raise ValueError('Unsupported label type {}'.format(type(label)))

    def __getitem__(self, bit):
        if bit is Character.BIT_0 or bit is 0:
            return self.left
        if bit is Character.BIT_1 or bit is 1:
            return self.right
        raise Exception('Invalid item {}'.format(bit))

    @property
    def label(self):
        if self.elemental:
            return self.value
        return self._label

    @classmethod
    def build_tree(cls, character_list):
        character_heap = Heap()
        for character in character_list:
            character_heap.insert(character)
        while character_heap.size() > 1:
            min_a = character_heap.pop()
            min_b = character_heap.pop()
            new_label = min_a._label | min_b._label
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
        decoded, index = self.decode_next(bit_array, 0)
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
        if c in self.left._label:
            return Character.BIT_0
        elif c in self.right._label:
            return Character.BIT_1
        else:
            raise Exception

    def code(self, c):
        if self.elemental:
            return Character.EMPTY
        bit = self.direction(c)
        return bit + self[bit].code(c)

    def __repr__(self):
        cadena = 'Character(\'' + ''.join(self.label) + '\',' + str(self.weight) + ')'
        return cadena
