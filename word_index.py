class SimpleAcceptor:
    def __init__(self, words, excludes, min_coverage_percent):
        self.words = words
        self.excludes = excludes
        self.set_min_coverage(min_coverage_percent)

    def set_min_coverage(self, min_cov):
        self.min_coverage_percent = min_cov
        self.min_words = round((self.min_coverage_percent/100)*len(self.words))

    def accept(self, word):
        if not any(word in s for s in self.excludes):
            count = self.count(word)
            return count >= self.min_words
        return False

    def count(self, word):
        return sum(word in s for s in self.words)

    def coverage(self, word):
        return self.count(word)*100 / len(self.words) # Big call here, 162/246 secs total, 75 seconds in sum from 87078 calls, 86 in generator from 870867078 calls


class WordSetAcceptor(SimpleAcceptor):
    def __init__(self, *args):
        super().__init__(*args)
        self.sets = make_sets(self.words)

    def get_set(self, id):
        if id not in self.sets:
            # this is safe, as all single element sets are already created. We just need at least two
            new_set = self.sets[id[0]].intersection(*list([self.sets[c] for c in id[1:]]))
            if len(new_set) < self.min_words:
                new_set = set() # Blank this case for faster execution; no need to scan if it can never be enough
            self.sets[id] = new_set
        return self.sets[id]

    def lookup(self, word):
        chars = set(word)
        id = ''.join(sorted(chars))
        to_check = self.get_set(id)
        return to_check

    def count(self, word):
        return sum(word in w for w in self.lookup(word))


def make_sets(words):
    character_sets = {}
    for w in words:
        for c in set(w):
            if c not in character_sets:
                character_sets[c] = set()
            character_sets[c].add(w)
    return character_sets
