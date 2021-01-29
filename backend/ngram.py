from math import log10


class Heuristic(object):
    def __init__(self, ngram_file, sep=" "):
        key = ""
        self.ngrams = {}

        # Get the occurrences count from the file
        for line in open(ngram_file):
            key, count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())

        # Calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        score = 0
        ngrams = self.ngrams.__getitem__

        # Compute the heuristic values
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor

        return score