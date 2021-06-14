#!/usr/bin/env python3
from collections import namedtuple

# Data Structures

## String Store
## A single long string containing all strings needed
string_store = []

## String Store Pointer
## An index and length into the string store
SSPointer = namedtuple('SSPointer', ['index', 'size'])

## Button Bits
## Keys represented as a single number for efficiency
class ButtonBits:
    LENGTH = 22
    def __init__(self, bits=None):
        if bits:
            self.bits = bits
        else:
            self.bits = [False] * ButtonBits.LENGTH
        assert len(bits) == ButtonBits.LENGTH

## String Chains
## A map of Button Bits Arrays to String Store Pointers
string_chains = {
    # Keys are ButtonBit lists, entries are SSPointer lists
}

def main():
    pass

if __name__ == '__main__':
    main()
