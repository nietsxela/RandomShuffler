import math
from scipy.stats import binom, bernoulli
import numpy as np


class AShuffler:

    @staticmethod
    def shuffle(num: int) -> np.array:
        cut_loc = AShuffler.cut(num)
        new_indexes = AShuffler.riffle(num, cut_loc)
        return np.array(new_indexes)

    @staticmethod
    def apply_shuffle(input_list: np.array) -> np.array:
        shuffle = AShuffler.shuffle(len(input_list))
        return input_list[shuffle]

    @staticmethod
    def cut(deck_length: int) -> int:
        # binom.rvs(52, 0.5, size=10000)
        return binom.rvs(deck_length, 0.5)

    @staticmethod
    def riffle(deck_length: int, cut_location: int) -> list:
        # iterlace from each of the two decks, based on following idea:
        # draw from top of deck x with probability: S_x / (S_x + (S_n - S_x))
        # where S_x is the remaining cards in x and S_n is the remaining cards all decks that havent been allocated
        # for 2 decks this means we draw from deck x with S_x / (S_x + S_y) and deck with S_y / (S_x + S_y)
        # repeat until both decks are depleted fully
        i = 0
        j = cut_location
        output_deck = []
        for c in range(deck_length):
            s_x = cut_location - i
            s_y = deck_length - j
            deck_prob = s_y / (s_x + s_y)
            choice = bernoulli.rvs(deck_prob)
            if choice == 0:
                output_deck.append(i)
                i += 1
            else:
                output_deck.append(j)
                j += 1

        return output_deck

    @staticmethod
    def count_rising_sequences(deck: np.array) -> int:
        counter = 0
        rising_sequences = 0
        while counter < len(deck) - 1:
            rising_sequences += 1
            for card in deck:
                if card == counter + 1:
                    counter += 1

        return rising_sequences

    @staticmethod
    def n_choose_k(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return math.factorial(n) / (math.factorial(n - k) * math.factorial(k))

