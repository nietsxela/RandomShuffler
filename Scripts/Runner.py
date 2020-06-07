import random
import scipy.stats as stats

from RandomDeterminers.TopRandomDeterminer import TopRandomDeterminer
from RandomDeterminers.StreakRandomDeterminer import StreakRandomDeterminer
from RandomDeterminers.FreqRandomDeterminer import FreqRandomDeterminer
from Shufflers.AShuffler import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import rv_discrete


##### determining how random a deck is based on ARandomDeterminer
# each can take in a deck and see how well its internal guessing algorithm does
# how_random and is_random are comparing the amount it could guess on this iter vs distribution
num_cards = 52
ordered_deck = np.arange(num_cards)

uniform_freq = np.ones((num_cards, num_cards)) / num_cards

total_shuffles = 13
iters = 10000
card_matrix = np.zeros([total_shuffles + 1, iters, num_cards])

for i in range(iters):
    card_matrix[0, i, :] = ordered_deck

# these are determiners
determiners = {}

determiners["Freq"] = FreqRandomDeterminer(num_cards, iters)
print("Randomizer using freq set")

determiners["Streak"] = StreakRandomDeterminer(num_cards, iters)
print("Randomizer using streak set")

determiners["Top"] = TopRandomDeterminer(num_cards, iters)
print("Randomizer using top set")

all_guesses = np.zeros([total_shuffles, iters, len(determiners)])

diffs = []
kstests = []
for current_shuffle_num in range(1, total_shuffles + 1):
    print("Shuffle number: " + str(current_shuffle_num))
    for i in range(iters):
        shuf_new = AShuffler.shuffle(num_cards)
        new_deck = card_matrix[current_shuffle_num - 1, i, :][shuf_new]

        j = 0
        for key in determiners.keys():
            all_guesses[current_shuffle_num - 1, i, j] = determiners[key].how_random(new_deck, current_shuffle_num)
            j += 1

        card_matrix[current_shuffle_num, i, :] = new_deck

    if "Freq" in determiners.keys():
        freq = determiners["Freq"].frequencies_by_position[current_shuffle_num]
        diffs.append(np.sum(np.square(np.subtract(freq, uniform_freq))))
        kstests.append(stats.kstest(freq.flatten(), "uniform")[0])

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(nrows=3, ncols=len(determiners))
ax0 = fig.add_subplot(gs[0, :])
average = []
i = 0
for key in determiners.keys():
    det = determiners[key]
    print("Plotting Chart: " + str(det.get_name()))
    ax0.plot(range(1, total_shuffles + 1), np.mean(all_guesses[:, :, i], 1), label=det.get_name()) # average across all iters per shuffle
    ax1 = fig.add_subplot(gs[1, i])
    det.print_stats(ax1)
    ax1.set_title(det.get_title())
    ax1.set_yticklabels([])
    average.append(det.df.mean()[0])
    i += 1


ax0.set_title("Amount Correct by naive algorithm after each shuffle")
ax0.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
ax0.yaxis.set_major_locator(ticker.MultipleLocator(3.0))
ax0.set(xlabel='Shuffles')
avg = (sum(average) / len(determiners))
ax0.plot(range(1, total_shuffles + 1), [avg for x in range(total_shuffles)], label="average: " + str(round(avg, 2)))
ax0.legend()
ax0.grid(True)

if "Freq" in determiners.keys():
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.set_title("Statistics for distribution after each shuffle")
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax2.set(xlabel='Shuffles')
    ax2.plot(range(1, total_shuffles + 1), diffs, label="sum squared diff")
    ax2.legend()
    ax2.grid(True)

    ax3 = fig.add_subplot(gs[2, 1])
    ax3.set_title("Statistics for distribution after each shuffle")
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax3.set(xlabel='Shuffles')
    ax3.plot(range(1, total_shuffles + 1), kstests, label="kstest")
    ax3.legend()
    ax3.grid(True)

plt.show()

# see number of rising sequences in a random deck on average
num_rising_sequences = []
iters = 100
for x in range(iters):
    if x % 1000 == 0:
        print(x)
    tgt = np.arange(num_cards)
    random.shuffle(tgt)
    rs = AShuffler.count_rising_sequences(tgt)
    num_rising_sequences.append(rs)


# Eulerean numbers
num_cards = 52
A_nr = {}
for r in range(1, (num_cards//2) + 1):
    val = math.pow(r, num_cards) - sum(
        [(A_nr[y] * AShuffler.n_choose_k(num_cards + r - y, num_cards)) for y in range(1, r)])
    A_nr[r] = val
    A_nr[num_cards + 1 - r] = val

U_pi = 1 / math.factorial(num_cards)

var_distances = []
max_shuffles = 10
for k in range(0, max_shuffles):
    print("num shuffles: " + str(k))
    running_sum = 0
    for r in range(1, num_cards + 1):
        numerator = AShuffler.n_choose_k(num_cards + math.pow(2, k) - r, num_cards)
        denom = math.pow(2, num_cards * k)
        running_sum += A_nr[r] * abs(numerator / denom - U_pi)
    var_distances.append(running_sum / 2)
    print(var_distances)
