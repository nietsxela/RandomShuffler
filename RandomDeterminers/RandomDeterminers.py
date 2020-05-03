from Items.Items import Deck
import random
import heapq
import pandas as pd
import matplotlib.pyplot as plt


## methods to determine if something is random, should take in a list and return true of false

class AlexRandomizer:
    def __init__(self):
        self.a_list = Deck(1).cards
        self.random_list = Deck(1).cards
        random.shuffle(self.random_list)
        sames = 0
        for i in range(len(self.a_list)):
            sames += 1 if self.a_list[i] == self.random_list[i] else 0


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
            first = ListNode(self.input_list, self.start_pos, loc-1)
        else:
            first = ListNode(self.input_list, loc, loc)
            first.is_valid = False

        if loc + 1 <= self.end_pos:
            second = ListNode(self.input_list, loc + 1, self.end_pos)
        else:
            second = ListNode(self.input_list, loc, loc)
            second.is_valid = False

        # print("Splitting: " + str(self) + " into: " + str(first) + " and " + str(second))
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


total = 0
iters = 10000
amount_correct = []
a = 1
for x in range(iters):
    target_list = Deck(a).cards
    guess_list = Deck(a).cards  # guess in order
    random.shuffle(target_list)  # shuffle tgt list

    node = ListNode(guess_list, 0, len(guess_list) - 1)
    map_of_lists = {0: node}  # indexed by starting location of list
    node_heap = [node]  # this is the heap we will use to find longest continuous list of potential guesses

    sames = 0
    guessed_in_list = []
    for i in range(len(target_list)):
        target_card = target_list[i]
        total_len = 0
        # print(guessed_in_list)
        for l in node_heap:
            if l.is_valid:
                total_len += l.length

        # print(total_len, i, a)
        assert total_len + i == (52 * a)

        while True:
            nl = heapq.heappop(node_heap)
            guess = nl.get_guess()
            if nl.is_valid:  # valid guess
                heapq.heappush(node_heap, nl)
                break
            else:
                pass
                # print("REMOVING INVALID: " + str(nl.first) + " end pos " + str(nl.end_pos))

        if target_card == guess:
            sames += 1

        loc_of_true = guess_list.index(target_list[i])
        guessed_in_list.append(loc_of_true)
        # print("Guess number: " + str(i) + " guess: " + str(guess) + " target card: " + str(target_card) + ". guess is at position " + str(loc_of_true))
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

    amount_correct.append(sames)
    total += sames



df = pd.DataFrame(amount_correct)




fig, ax = plt.subplots()

xlim = (0, 15)
ylim = (0, 3000)
ax.set(xlim=xlim, ylim=ylim)

# Generate a normal distribution, center at x=0 and y=5
num_bins = 13
n, bins, patches = ax.hist(amount_correct, num_bins)

print(df.describe())
print(total*1.0/iters)
plt.show()


# 1 std move.  If we get more than this then it is significant prob of getting right - 6.189067
#count  10000.000000
#mean       4.520700
#std        1.668367
#min        1.000000
#25%        3.000000
#50%        4.000000
#75%        6.000000
#max       13.000000

