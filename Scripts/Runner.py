from RandomDeterminers import RandomDeterminers2
from Shufflers.AShuffler import *
from Items.Items import Deck
import matplotlib.pyplot as plt

cards = np.array(Deck(1).cards)


#todo make randomDeterminers compatible with np arrays

o = np.arange(len(cards))

num_cards = len(cards)
num_shuffles = 25
iters = 10000
a = np.zeros([num_shuffles + 1, iters, num_cards])

for i in range(iters):
    a[0, i, :] = o

last = 100
num_correct = 99
print("Random Cutoff is: " + str(RandomDeterminers2.random_cutoff))
# for current_shuffle in range(num_shuffles):
current_shuffle = 0
avg_num_correct = []
while num_correct < last:
    last = num_correct
    random_list = []
    for i in range(iters):
        o_new = AShuffler.shuffle(cards)
        new_deck = a[current_shuffle, i, :][o_new]
        how_random = AShuffler.how_random(o.tolist(), new_deck.tolist())
        random_list.append(how_random)
        a[current_shuffle + 1, i, :] = new_deck

    num_correct = sum(random_list) / len(random_list)
    avg_num_correct.append(num_correct)
    print("After " + str(current_shuffle + 1) + " shuffles got: " + str(num_correct) + ". Is random: "
          + str(num_correct < RandomDeterminers2.random_cutoff))
    current_shuffle += 1

plt.plot(avg_num_correct)
plt.plot([RandomDeterminers2.random_cutoff for x in avg_num_correct])
plt.ylabel('Amount of correct guesses on average by naive Algorithm')
plt.ylabel('Shuffles')
plt.show()