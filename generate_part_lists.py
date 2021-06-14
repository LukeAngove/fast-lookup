from difflib import SequenceMatcher, Match
from typing import List

def make_match_list(wlist, word_list, preference_factor=0):
    matcher = SequenceMatcher()
    return {w: get_matches(matcher, wlist, w, preference_factor) for w in word_list}

def get_matches(matcher, wlist, word, preference_factor):
    return _get_matches(matcher, wlist, word, True, True, preference_factor)

def _get_matches(matcher : SequenceMatcher, wlist : List[str], word : str, prefer_start : bool = True, prefer_end : bool = True, preference_factor : int = 0):
    if word == '':
        return []

    matcher.set_seq2(word)

    current_match = Match(0, 0, 0)
    is_start = False
    is_end = False
    current_idx = 0
    # Assume wlist is ordered with longest sequences first
    for i, w in enumerate(wlist):
        lw = len(w)
        # We can't ever get a better match, so stop here
        if current_match.size > lw:
            break

        matcher.set_seq1(w)
        r = matcher.find_longest_match(0, lw, 0, len(word))
        if r.size > current_match.size:
            is_start = (r.a == 0)
            is_end = (r.a + r.size) == lw
            current_idx = i
            current_match = r
    me = (current_idx, current_match, is_start, is_end)

    matches = _get_matches(matcher, wlist, word[:current_match.b], prefer_start, is_start, preference_factor)
    matches.append(me)
    after = _get_matches(matcher, wlist, word[(current_match.b + current_match.size):], is_end, prefer_end, preference_factor)
    matches.extend(after)

    return matches
