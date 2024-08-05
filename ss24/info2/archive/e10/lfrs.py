import sys
import matplotlib.pyplot as plt
from collections import Counter


class LFSR:
    def __init__(self, seed):
        if not all(ord('A') <= ord(c) <= ord('Z') for c in seed):
            raise ValueError('Seed must consist of uppercase alphabetic characters')

        self.register = list(seed)
        self.alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.a_len = len(self.alphabet)

    def f(self, a, b):
        """Caesar Funktion"""
        shift_value = self.alphabet.index(b) + 1
        c = self.alphabet[(self.alphabet.index(a) + shift_value) % self.a_len]
        return c

    def shift(self):
        """
        Der Algorithmus zum Verschieben des Registers
        Wir schieben `b` von rechts ein.
        """
        b = self.f(self.f(self.register[1], self.register[3]), self.f(self.register[-2], self.register[-1]))
        # rechts
        self.register.append(b)
        x = self.register.pop(0)
        return x

    def generate_sequence(self, length):
        return ''.join(self.shift() for _ in range(length))


def plot_character_counts(sequence):
    counter = Counter(sequence)

    # sort in alphabetical order
    items = sorted(counter.items())

    # unzip the into a list of characters and a list of counts
    characters, counts = zip(*items)

    # create a bar chart
    plt.bar(characters, counts)

    # set the title and labels
    plt.title("Character Counts")
    plt.xlabel("Character")
    plt.ylabel("Count")

    # show the plot
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python lfsr.py <seed> <length> [-p]")
        sys.exit(1)

    seed = sys.argv[1]
    try:
        n = int(sys.argv[2])
    except ValueError:
        print("Length must be an integer")
        sys.exit(1)

    lfsr = LFSR(list(seed))

    try:
        sequence = lfsr.generate_sequence(n)
        print(sequence)
        if "-p" in sys.argv[3:]:
            plot_character_counts(sequence)
    except ValueError as e:
        print(e)
