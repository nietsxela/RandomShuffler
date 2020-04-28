import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value_str = self.get_value_str(rank)
        self.point_value = self.get_value(rank)

    @staticmethod
    def get_value_str(rank):
        if rank == 1:
            return "A"
        elif rank == 11:
            return "J"
        elif rank == 12:
            return "Q"
        elif rank == 13:
            return "K"
        elif rank == -1:
            return "Joker"
        else:
            return str(rank)

    @staticmethod
    def get_value(rank):
        ## mainly for blackjack or canasta
        return rank

    @staticmethod
    def get_suit(suit):
        if suit == 0:
            return "Spades"
        elif suit == 1:
            return "Clubs"
        elif suit == 2:
            return "Hearts"
        elif suit == 3:
            return "Diamonds"
        return ""

    def is_ace(self):
        return self.rank == 1

    def is_joker(self):
        return self.rank == -1

    def __str__(self):
        if self.suit < 0:
            return self.value_str
        return self.value_str + " of " + self.get_suit(self.suit)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return NotImplemented


class Deck:
    CARDS_PER_DECK = 52
    CARDS_PER_DECK_WITH_JOKERS = 54

    def __init__(self, number_of_decks, jokers=False):
        self.removed_cards = 0
        number_of_decks = max(number_of_decks, 1)  # at least one deck
        self.total_cards = number_of_decks * self.CARDS_PER_DECK_WITH_JOKERS if jokers else self.CARDS_PER_DECK
        self.cards = self.reset_deck(number_of_decks, jokers)
        self.current = iter(self.cards)
        self.shuffle_method = None

    @staticmethod
    def reset_deck(num, jokers=False):
        cards = []
        for n in range(num):
            for x in range(1, 14):
                for y in range(4):
                    cards.append(Card(y, x))
        if jokers:
            cards.append(Card(-1, -1))
            cards.append(Card(-1, -1))

        return cards

    # def shuffle(self):
    #     self.removed_cards = 0
    #     self.current = iter(self.cards)
    #
    #     if self.shuffle_method is not None:
    #         self.shuffle_method.shuffle(self.cards)
    #     else:
    #         random.shuffle(self.cards)

    def apply_shuffle_method(self, shuffle_method):
        self.shuffle_method = shuffle_method

    def draw(self):
        if self.remaining_cards() == 0:
            self.shuffle()
        self.removed_cards += 1
        return next(self.current)

    def print_deck(self):
        i = 0
        for c in self.cards:
            print(c)
            i += 1
        print("total cards: " + str(i))

    def remaining_cards(self):
        return self.total_cards - self.removed_cards

# d = Deck(1, True)
# d.print_deck()
