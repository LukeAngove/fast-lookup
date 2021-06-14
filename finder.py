#!/usr/bin/env python3
from typing import List

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

def find_strings(words : List[str], generator, exclude : List[str] = None):
    if exclude is None:
        exclude = []
    # Use different arrays to make checking subs easier.
    subs = []
    coverages = []

    for checking in generator:
        usable = not any(checking in s for s in exclude) and checking not in subs
        if usable:
            coverage = sum(checking in s for s in words) / len(words)
            if coverage > 0:
                subs.append(checking)
                coverages.append(coverage)
    subs = list(zip(coverages, subs))

    subs.sort(reverse=True)
    return subs

# Assume words are sorted before use.
def generate_parts(words, min_words_to_count):
    wlist = []
    for i in range(max(len(w) for w in words), 0, -1):
        wgen = word_list_generator(words, i)
        r = find_strings(words, wgen, wlist)
        r = [w
            for w in r
            if w[0] > (min_words_to_count/len(words))
                or len(w[1]) == 1] # Make sure every word is possible in dict; include any character not used so far.
        if len(r):
            ws = list(zip(*r))[1]
            wlist.extend(ws)
    return wlist
 