

from bitarray import bitarray
from heap import Heap


# Huffman tree
class Character:

    def __init__(self, label, weight, elemental=False):
        self.weight = weight
        self.label = label
        self.left = None
        self.right = None
        self.elemental = elemental

    def __getitem__(self, bit):
        if bit == 0:
            return self.left
        if bit == 1:
            return self.right

    @classmethod
    def build_tree(cls, character_list):
        character_heap = Heap()
        for character in character_list:
            character_heap.insert(character)
        while character_heap.size() > 1:
            min_a = character_heap.pop()
            min_b = character_heap.pop()
            new_label = list(min_a.label)
            new_label.extend(min_b.label)
            new_weight = min_a.weight + min_b.weight
            character_tree = Character(new_label, new_weight)
            character_tree.left = min_a
            character_tree.right = min_b
            character_heap.insert(character_tree)
        return character_heap.pop()

    def decode(self, bit_array, index=0):
        bit = bit_array[index]
        if self[bit].elemental:
            return self[bit].label[0], index + 1
        return self[bit].decode(bit_array, index=index + 1)

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
