import numpy as np
from abc import ABC, abstractmethod
import matplotlib.ticker as ticker
import pandas as pd
import random


class ARandomDeterminer(ABC):

    def __init__(self, num_cards: int = 52, iters: int = 100):
        self.num_cards = num_cards
        self.iters = iters
        self.amount_correct = self.setup()
        self.df = pd.DataFrame(self.amount_correct)

    def setup(self) -> list:
        total = 0
        amount_correct = []
        for x in range(self.iters):
            tgt = np.arange(self.num_cards)
            random.shuffle(tgt)  # shuffle tgt list
            sames = self.make_guesses(tgt)
            amount_correct.append(sames)
            total += sames

        return amount_correct

    @abstractmethod
    def get_title(self) -> str:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def make_guesses(self, target_list: np.array, shuffle: int = 0) -> int:
        ...

    def get_cutoff(self) -> float:
        return self.df.mean + self.df.std

    def how_random(self, deck: np.array, shuffles: int = 0):
        # many ways to do this but I think the simplest is to see if the guesser can get more than
        # 2 std better than mean of simple algorithm
        # RandomDeterminers will tell us mean and std of simple algorithm guesser
        return self.make_guesses(deck, shuffles)

    def is_random(self, deck: np.array, shuffles: int = 0):
        # many ways to do this but I think the simplest is to see if the guesser can get more than
        # 2 std better than mean of simple algorithm
        # RandomDeterminers will tell us mean and std of simple algorithm guesser
        return self.how_random(deck, shuffles) <= self.get_cutoff()

    def print_stats(self, ax):
        num_bins = 10
        ax.hist(self.amount_correct, bins=num_bins)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
        ax.set(xlabel='Correct Guesses on random deck')
        print(self.df.describe())
