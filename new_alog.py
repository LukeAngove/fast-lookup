#!/usr/bin/env python3

from os import replace
from typing import List
from pprint import pprint
from difflib import SequenceMatcher, Match
import yaml

class SequenceBox:
    def __init__(self, boxed):
        self.me = boxed
    
    def is_record(self):
        return isinstance(self.me, SequenceRecord)
    
    @staticmethod
    def make_record(word):
        return SequenceBox(SequenceRecord(word))
    
    def add_subsequence(self, start, length):
        self.me.add_subsequence(start, length)
    
    def __str__(self):
        return str(self.me)
    
    def __add__(self, other_box):
        new = SequenceRecord(str(self) + str(other_box))
        new.subsequences.extend(self.me.subsequences)
        new_me = new.add_subsequence(0, len(self))
        new.subsequences.extend([]) # Do I deal with the references here? More boxes?
        new_other = new.add_subsequence(len(self), len(other_box))
        other_box.me = new_other
        self.me = new_me
        return SequenceBox(new)
    
    def __len__(self):
        return len(self.me)

class SequenceRecord:
    def __init__(self, seq):
        self.seq = seq
        self.subsequences = []

    def add_subsequence(self, start, length):
        new = SequenceReference(self, start, length)
        self.subsequences.append(new)
        return new
    
    def __str__(self):
        return self.seq

    def __len__(self):
        return len(self.seq)

class SequenceReference(SequenceRecord):
    def __init__(self, target, start, length):
        self.target = target
        self.start = start
        self.length = length
    
    def add_subsequence(self, start, length):
        return self.target.add_subsequence(self.start+start, length)
    
    def __str__(self):
        return str(self.target)[self.start:self.start+len(self)]
    
    def __len__(self):
        return self.length

class Sequences:
    def __init__(self, words):
        chars = get_char_set(words)
        self.items = {c:SequenceBox.make_record(c) for c in chars}
    
    def join(self, a, b):
        self.items[a+b] = self.items[a] + self.items[b]
     
    def record_matches(self, word):
        matcher = SequenceMatcher()
        matcher.set_seq2(word)
        wlen = len(word)
        matches = []
        for r in self.records():
            s = str(r)
            matcher.set_seq1(s)
            match = matcher.find_longest_match(0, len(s), 0, wlen)
            if match.size > 0:
                matches.append(match)
        return matches

    def size_to_add(self, to_add):
        if to_add in self.items:
            return 0
        
        if any(to_add in str(w) for w in self.records):
            return 0
        
        #matches = self.record_matches(to_add)
        # Get all overlapping matches with compatible edges.
        return len(to_add) # Simple implementation; just add it
    
    def add_record(self, to_add):
        self.items[to_add] = SequenceBox.make_record(to_add)

    @property
    def records(self):
        return [w for w in self.items.values() if w.is_record()]

    def size(self):
        # Assume 1 byte each
        return sum(len(w) for w in self.records)

def get_char_set(words : List[str]):
    values = set()
    for w in words:
        a = set(w)
        values = values.union(set(w))
    return str(list(values))

class EdgeCounter:
    def __init__(self, words):
        self.words = [list(w) for w in words]
        self.counts = dict()
        self.part_size = 3 # 2 byte start and 1 byte length, 
        self.chars = get_char_set(words)
    
    def words_len(self):
        return sorted((len(w), w) for w in self.words)

    def words_size(self):
        return sum(len(w) for w in self.words)*self.part_size
    
    def count(self):
        # Only do this if anything changed (we did a merge)
        if not self.counts:
            self.counts = dict()
            for i, w in enumerate(self.words):
                if len(w) > 1:
                    for j, (a,b) in enumerate(zip(w[:-1], w[1:])):
                        val = a+b
                        if val not in self.counts:
                            self.counts[val] = []
                        self.counts[val].append((i, j))

    def sorted_counts(self):
        self.count()
        return sorted([(len(v),k) for k,v in self.counts.items()], reverse=True)

    def propose_merge(self):
        # Only do replacements that don't affect the same letters; then we can't have an issue with overlaping merges.
        # We can check just the boundries; if they are safe, then everything should be safe.
        touched = set()
        to_replace = []
        for w in self.sorted_counts():
            rep = w[1]
            if rep[0] not in touched and rep[-1] not in touched:
                to_replace.append(w)
                touched.add(rep[0])
                touched.add(rep[-1])
                if touched == self.chars:
                    break # Early exit if we've touched all characters
        return to_replace 

    def do_merge(self, to_replace):
        # Do in reverse order, so that we don't interfere with ourselves; starting at the end of each word preseves left indecies
        # Word order doesn't matter, so that may as well be backwards too.
        replace_list = sorted([v for r in to_replace for v in self.counts[r[1]]], reverse=True)

        for i, j in replace_list:
            self.words[i][j] = self.words[i][j] + self.words[i][j+1] # Merge elements
            self.words[i].pop(j+1) # Remove the second element
        self.counts = None # Counts are now invalid

def merge_shrink_size(to_merge):
    return sum(3*m[0] for m in to_merge)

def size_str(size):
    return f'{size}B {size/1024}k {size/(1024*1024)}M'

def minimise_words(words : List[str]):
    seqs = Sequences(words)
    edge_counter = EdgeCounter(words)
    #pprint(edge_counter.sorted_counts())
    #print(list(str(w) for w in seqs.items.values()))

    size = edge_counter.words_size()
    print('pre-words:', size_str(size))
    size = seqs.size()
    print('pre-dict:', size_str(size))

    n_to_merge = 1
    i=0
    while n_to_merge:
        i+=1
        print(f'Merge {i}')
        to_merge = edge_counter.propose_merge()
        print('Proposed:', len(to_merge))
        to_merge = list(filter(lambda a: seqs.size_to_add(a[1])<a[0], to_merge))
        n_to_merge = len(to_merge)
        print('Accepted:', n_to_merge)
        print(to_merge)
        print('Merge shrink size:', size_str(merge_shrink_size(to_merge)))
        for m in to_merge:
            seqs.add_record(m[1])
        edge_counter.do_merge(to_merge)

        esize = edge_counter.words_size()
        print('post-words:', size_str(esize))
        ssize = seqs.size()
        print('post-dict:', size_str(ssize))
        print('total: ', size_str(esize+ssize))
    pprint(edge_counter.words_len())
    pprint(list(str(w) for w in seqs.items.values()))

if __name__ == '__main__':
    with open('words.yml') as f:
        words = yaml.safe_load(f.read())
    minimise_words(words) # Required to be sorted for generate parts.

