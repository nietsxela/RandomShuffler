from Items.Items import Deck
from scipy.stats import binom, bernoulli
import numpy as np
from RandomDeterminers.RandomDeterminers2 import make_guesses, random_cutoff

class AShuffler:

    @staticmethod
    def shuffle(my_list):
        # todo must be implemented and return a list
        # todo call cut and riffle methods
        cut_loc = AShuffler.cut(len(my_list))
        new_indexes = AShuffler.riffle(len(my_list), cut_loc)
        return np.array(new_indexes)

    @staticmethod
    def apply_shuffle(list, indexes):
        return

    @staticmethod
    def cut(deck_length):
        # todo cut according to a binomial distribution
        # binom.rvs(52, 0.5, size=10000)
        return binom.rvs(deck_length, 0.5)

    @staticmethod
    def riffle(deck_length, cut_location):
        # todo iterlace from each of the two decks, based on following idea:
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
            # print("s_x: " + str(s_x) + " s_y: " + str(s_y) + " deck_prob: " + str(deck_prob))
            choice = bernoulli.rvs(deck_prob)
            # print("Choice: " + str(choice))
            if choice == 0:
                output_deck.append(i)
                i += 1
            else:
                output_deck.append(j)
                j += 1

        return output_deck

    @staticmethod
    def is_random(deck, prev_deck):
        # many ways to do this but I think the simplest is to see if the guesser can get more than
        # 2 std better than mean of simple algorithm
        # RandomDeterminers will tell us mean and std of simple algorithm guesser
        return AShuffler.how_random(deck, prev_deck) <= random_cutoff

    @staticmethod
    def how_random(deck, prev_deck):
        # many ways to do this but I think the simplest is to see if the guesser can get more than
        # 2 std better than mean of simple algorithm
        # RandomDeterminers will tell us mean and std of simple algorithm guesser
        return make_guesses(deck, prev_deck)

