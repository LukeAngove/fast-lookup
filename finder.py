#!/usr/bin/env python3
from typing import List
from word_index import SimpleAcceptor, WordSetAcceptor

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def brute_force_generator(values : str, size : int):
    digit_max = len(values)
    
    for checking in range(digit_max * size):
        c = numberToBase(checking, digit_max)
        result = ''.join(values[d] for d in c)
        yield result


# Assume words is sorted by size, so we can return early for long sizes
def word_list_generator(words : List[str], size : int):
    for word in words:
        if len(word) >= size:
            for w in [word[i:i+size] for i in range(len(word)-size+1)]:
                yield w
        else:
            break

def find_strings(generator, acceptor : SimpleAcceptor):
    # Use different arrays to make checking subs easier.
    subs = set()

    for checking in generator:
        # Still check if in set to avoid the (expensive) acceptor check on duplicates.
        # This optimisation means we can't use a generator expression.
        if checking not in subs and acceptor.accept(checking):
            subs.add(checking)
    return subs

# Assume words are sorted by length (longest first) before use for word_list_generator_call.
# Better to sort ahead of time to keep it immutable here.
def generate_parts(words, accept_percent):
    wlist = []
    acceptor = WordSetAcceptor(words, wlist, accept_percent)
    # Iterate backwards, as big sequences contain smaller; want to remove overlap
    for i in range(max(len(w) for w in words), 0, -1):
        if i == 1:
            # Make sure every word is possible in dict; include any character not used so far.
            acceptor.set_min_coverage(0)
        wgen = word_list_generator(words, i)
        r = find_strings(wgen, acceptor)
        wlist.extend(r)
    return wlist
