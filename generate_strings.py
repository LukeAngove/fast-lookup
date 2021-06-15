#!/usr/bin/env python3
from finder import generate_parts
from generate_part_lists import make_match_list
import yaml
from pprint import pprint

if __name__ == '__main__':
    with open('words.yml') as f:
        words = yaml.safe_load(f.read())[:10000]
    words.sort(key=len, reverse=True) # Required to be sorted for generate parts.

    wlist = generate_parts(words, 0.5) # If it's in 0.5% of words

    matches = make_match_list(wlist, words)
    print(len(wlist), wlist)
    print(dict({k: len(v) for k,v in matches.items()}))
    print(max(len(v) for v in matches.values()))
