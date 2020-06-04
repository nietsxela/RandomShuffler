import heapq
import numpy as np
from ARandomDeterminer import ARandomDeterminer


class StreakRandomDeterminer(ARandomDeterminer):

    # count  10000.000000
    # mean       4.520700
    # std        1.668367
    # min        1.000000
    # 25%        3.000000
    # 50%        4.000000
    # 75%        6.000000
    # max       13.000000

    def make_guesses(self, target_list: np.array, shuffle: int = 0) -> int:
        num_cards = len(target_list)
        guess_list = np.arange(num_cards)
        node = ListNode(guess_list, 0, len(guess_list) - 1)
        map_of_lists = {0: node}  # indexed by starting location of list
        node_heap = [node]  # this is the heap we will use to find longest continuous list of potential guesses
        sames = 0
        guessed_in_list = []
        for i in range(len(target_list)):
            target_card = target_list[i]
            total_len = 0
            for l in node_heap:
                if l.is_valid:
                    total_len += l.length

            assert total_len + i == num_cards

            while True:
                nl = heapq.heappop(node_heap)
                guess = nl.get_guess()
                if nl.is_valid:  # valid guess
                    heapq.heappush(node_heap, nl)
                    break
                else:
                    pass

            if target_card == guess:
                sames += 1

            loc_of_true = int(np.where(guess_list == target_list[i])[0])
            guessed_in_list.append(loc_of_true)
            keys = (list(map_of_lists.keys()))
            keys.sort(reverse=True)
            for j in keys:
                if loc_of_true >= j:
                    n = map_of_lists.get(j)
                    if not n.is_valid:
                        pass
                    f, s = n.create_children(loc_of_true)
                    if f.length > 0:
                        map_of_lists[f.start_pos] = f
                        heapq.heappush(node_heap, f)

                    if s.length > 0:
                        map_of_lists[s.start_pos] = s
                        heapq.heappush(node_heap, s)

                    break
        return sames

    def get_title(self):
        return "Select first card in longest streak on random deck"

    def get_name(self):
        return "Streak"


class ListNode:

    def __init__(self, data_list, start_pos, end_pos):
        self.input_list = data_list
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.first = data_list[start_pos]
        self.length = self.end_pos - self.start_pos + 1
        self.is_valid = True

    def create_children(self, loc):
        if self.start_pos <= loc - 1:
            first = ListNode(self.input_list, self.start_pos, loc - 1)
        else:
            first = ListNode(self.input_list, loc, loc)
            first.is_valid = False

        if loc + 1 <= self.end_pos:
            second = ListNode(self.input_list, loc + 1, self.end_pos)
        else:
            second = ListNode(self.input_list, loc, loc)
            second.is_valid = False

        self.is_valid = False
        return first, second

    def get_guess(self):
        return self.first

    def __str__(self):
        return "list len: " + str(self.length) + " first card is " + str(self.first) + " at position: " + str(
            self.start_pos) + " ends at pos: " + str(self.end_pos) + ". Is Valid: " + str(self.is_valid)

    def __ge__(self, other):
        return self.length <= other.length

    def __gt__(self, other):
        return self.length < other.length

    def __le__(self, other):
        return self.length >= other.length

    def __lt__(self, other):
        return self.length > other.length
