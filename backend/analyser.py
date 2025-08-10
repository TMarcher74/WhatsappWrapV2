import re
from collections import Counter


class Analyser:
    pass

def get_most_used_words(messages, top_n: int = 10):
    word_counter = Counter()
    for msg in messages:
        words = re.findall(r'\b\w+\b', msg.lower())
        word_counter.update(words)
    return word_counter.most_common(top_n)
