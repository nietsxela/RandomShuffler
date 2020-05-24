import math
import random
from RandomDeterminers import RandomDeterminers2
from Shufflers.AShuffler import *
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


# todo make randomDeterminers compatible with np arrays

num_cards = 52

o = np.arange(num_cards)
AShuffler.count_rising_sequences(o)

total_shuffles = 25
iters = 10000
a = np.zeros([total_shuffles + 1, iters, num_cards])

for i in range(iters):
    a[0, i, :] = o

print("Random Cutoff is: " + str(RandomDeterminers2.random_cutoff))

current_shuffle_num = 0
avg_num_correct = []
for current_shuffle_num in range(total_shuffles):
    random_list = []
    for i in range(iters):
        shuf_new = AShuffler.shuffle(num_cards)
        new_deck = a[current_shuffle_num, i, :][shuf_new]
        how_random = AShuffler.how_random(o, new_deck)
        random_list.append(how_random)
        a[current_shuffle_num + 1, i, :] = new_deck

    num_correct = sum(random_list) / len(random_list)
    avg_num_correct.append(num_correct)
    print("After " + str(current_shuffle_num + 1) + " shuffles got: " + str(num_correct) + ". Is random: "
          + str(num_correct < RandomDeterminers2.random_cutoff))
    current_shuffle_num += 1

# see number of rising sequences in a random deck on average
num_rising_sequences = []
iters = 100000
for x in range(iters):
    if x % 1000 == 0:
        print(x)
    tgt = np.arange(num_cards)
    random.shuffle(tgt)
    rs = AShuffler.count_rising_sequences(tgt)
    num_rising_sequences.append(rs)


plt.plot(avg_num_correct)
plt.plot([RandomDeterminers2.random_cutoff for x in avg_num_correct])
plt.ylabel('Amount of correct guesses on average by naive Algorithm')
plt.ylabel('Shuffles')
plt.show()



A52 = np.zeros(52)
