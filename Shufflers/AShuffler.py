class AShuffler:

    @staticmethod
    def shuffle(my_list):
        # todo must be implemented and return a list
        # todo call cut and riffle methods
        pass

    @staticmethod
    def cut(my_list):
        # todo cut according to a binomial distribution
        pass

    @staticmethod
    def riffle(deck_1, deck_2):
        # todo iterlace from each of the two decks, based on following idea:
        # draw from top of deck x with probability: S_x / (S_x + (S_n - S_x))
        # where S_x is the remaining cards in x and S_n is the remaining cards all decks that havent been allocated
        # for 2 decks this means we draw from deck x with S_x / (S_x + S_y) and deck with S_y / (S_x + S_y)
        # repeat until both decks are depleted fully
        pass

    @staticmethod
    def is_random(deck):
        # todo
        # many ways to do this but I think the simplest is to see if the guesser can get more than
        # 2 std better than mean of simple algorithm
        # RandomDeterminers will tell us mean and std of simple algorithm guesser
        pass

