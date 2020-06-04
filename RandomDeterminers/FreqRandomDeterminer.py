import random
from ARandomDeterminer import ARandomDeterminer
from Shufflers.AShuffler import *
import numpy as np
from scipy.stats import rv_discrete


class FreqRandomDeterminer(ARandomDeterminer):

    def __init__(self, num_cards: int = 52, iters: int = 100):
        self.total_shuffles = 15
        self.frequencies_by_position = self.get_frequencies(num_cards, iters, self.total_shuffles)
        self.distributions = self.make_distributions(self.frequencies_by_position)
        ARandomDeterminer.__init__(self, num_cards, iters)

    def get_frequencies(self, num_cards: int = 52, iters: int = 100, total_shuffles: int = 15) -> np.array:
        card_matrix = np.zeros([total_shuffles + 1, iters, num_cards])
        ordered_deck = np.arange(num_cards)

        frequencies_by_position = np.zeros((total_shuffles + 1, num_cards, num_cards))
        frequencies_by_position[0, :, :] = np.eye(num_cards)
        for i in range(iters):
            card_matrix[0, i, :] = ordered_deck

        for current_shuffle_num in range(total_shuffles):
            print("Shuffle number: " + str(current_shuffle_num + 1))
            for i in range(iters):
                shuf_new = AShuffler.shuffle(num_cards)
                new_deck = card_matrix[current_shuffle_num, i, :][shuf_new]
                card_matrix[current_shuffle_num + 1, i, :] = new_deck

            this_shuffle = card_matrix[current_shuffle_num + 1, :, :]

            for position in range(num_cards):
                card_list = np.append(this_shuffle[:, position], ordered_deck)
                card, freq = np.unique(card_list, return_counts=True)
                freq -= 1
                frequencies_by_position[current_shuffle_num + 1, :, position] = np.divide(freq, iters)

        return frequencies_by_position

    def make_distributions(self, freqs: np.array) -> dict:
        output = {}
        for shuffle in range(freqs.shape[0]):
            pos = {}
            for position in range(freqs.shape[1]):
                d = freqs[shuffle, :, position]
                rv = rv_discrete(name="shuf_" + str(shuffle) + "_position_" + str(position), values=(range(len(d)), d))
                pos[position] = rv
            output[shuffle] = pos

        return output

    def get_title(self) -> str:
        return "Select card by most frequent at that position"

    def get_name(self) -> str:
        return "Freq"

    def make_guesses(self, target_list: np.array, shuffle: int = 15) -> int:
        guesses = []
        sames = 0
        shuffle = min(self.total_shuffles, shuffle)
        for position in range(len(target_list)):
            tries = 0
            dist = self.distributions[shuffle][position]
            guess = dist.ppf(random.random())
            while guess in guesses:
                tries += 1
                guess = dist.ppf(random.random())
                if tries >= 10:
                    break

            if guess in guesses:
                most_likely = sorted(range(len(dist.pk)), key=lambda k: dist.pk[k])
                for y in most_likely:
                    if y not in guesses:
                        guess = y
                        break

            guesses.append(target_list[position])
            if guess == target_list[position]:
                sames += 1

        return sames
