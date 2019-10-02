
from math import ceil

class bitarray:

    def __init__(self):
        self.length = 0
        self.number = 0

    def append(self, bit):
        if bit != 0 and bit != 1:
            raise ValueError('A bit can\'t be different from 0 or 1')
        mask = bit << self.length
        self.length += 1
        self.number |= mask

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.getslice(index)
        if self.length <= index or index <= -self.length:
            raise IndexError
        index = index % self.length
        mask = 1 << index
        bit = (self.number & mask) >> index
        return bit

    def to_bytes(self):
        # The format is as follows:
        # uint32_t big endian with the total amount of bits of the message
        # the bits of the message with the remaining bits of the last byte
        # unspecified
        length = self.length.to_bytes(length=4, byteorder='big')
        bytes_necessary = ceil(self.length/8)
        return length + self.number.to_bytes(length=bytes_necessary,
                                             byteorder='big')

    def getslice(self, index):
        if index.start is None:
            start = 0
        else:
            start = index.start % self.length
        if index.stop is None:
            stop = self.length - 1
        else:
            stop = index.stop % self.length
        step = index.step
        if step is None:
            step = 1
        bits = [self[i] for i in range(start, stop, step)]
        return self.__class__.from_list(bits)

    def throw(self, n):
        self.length -= n
        self.number = self.number >> n

    @classmethod
    def from_list(cls, bitlist):
        array = cls()
        array.extend(bitlist)
        return array

    @classmethod
    def from_number(cls, number):
        array = cls()
        array.number = number
        if number != 0:
            array.length = number.bit_length()
        else:
            array.length = 1
        return array

    def copy(self):
        array = self.__class__()
        array.number = self.number
        array.length = self.length
        return array

    def __add__(self, other):
        copy = self.copy()
        copy.extend(other)
        return copy

    def __setitem__(self, index, bit):
        if bit != 0 and bit != 1:
            raise ValueError('A bit can\'t be different from 0 or 1')
        if self.length <= index or index <= -self.length:
            raise IndexError
        index = index % self.length
        mask = 1 << index
        self.number &= ~mask
        self.number |= bit << index

    def extend(self, other):
        if isinstance(other, bitarray):
            number = other.number << self.length
            self.number += number
            self.length += other.length
        elif isinstance(other, list):
            for i in other:
                self.append(i)

    def __len__(self):
        return self.length

    def pop(self, index=None):
        if index is None:
            index = self.length - 1
        bit = self[index]
        self[index] = 0
        if index < self.length - 1:
            rest = -(1 << (index + 1))
            tail = (self.number & rest) >> 1
            self.number &= ~rest
            self.number += tail
        self.length -= 1
        return bit

    def __repr__(self):
        return ''.join([str(i) for i in list(self)])
