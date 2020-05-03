from Items.Items import Deck
import random
import pandas as pd
import matplotlib.pyplot as plt


def make_guesses(target_list, guess_list):

    sames = 0
    indexes_found = []
    current_guess_index = 0
    for i in range(len(target_list)):  # cycle through target cards and guess top card from guess
        target_card = target_list[i]
        while current_guess_index in indexes_found:
            current_guess_index += 1

        guess = guess_list[current_guess_index]
        if target_card == guess:
            sames += 1

        loc_of_true = -1
        while True:
            loc_of_true = guess_list.index(target_list[i], loc_of_true + 1)
            if loc_of_true not in indexes_found:
                indexes_found.append(loc_of_true)
                break

    return sames


def run():
    total = 0
    iters = 10000
    a = 1
    amount_correct = []
    for x in range(iters):
        tgt = Deck(a).cards
        random.shuffle(tgt)  # shuffle tgt list
        guess = Deck(a).cards  # guess in order
        sames = make_guesses(tgt, guess)
        amount_correct.append(sames)
        total += sames

    df = pd.DataFrame(amount_correct)

    fig, ax = plt.subplots()
    num_bins = 10
    n, bins, patches = ax.hist(amount_correct, bins=num_bins)

    xlim = (0, 10)
    ylim = (0, 3000)
    ax.set(xlim=xlim, ylim=ylim)

    print(df.describe())
    print(total*1.0/iters)
    plt.show()

random_cutoff = 3.572500 + 1.397691
#count  10000.000000
#mean       3.572500
#std        1.397691
#min        1.000000
#25%        3.000000
#50%        3.000000
#75%        4.000000
#max       10.000000
