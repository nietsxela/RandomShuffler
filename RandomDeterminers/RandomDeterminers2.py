from Items.Items import Deck
import random
import pandas as pd
import matplotlib.pyplot as plt

total = 0
iters = 1000
a = 3
amount_correct = []
for x in range(iters):
    target_list = Deck(a).cards
    guess_list = Deck(a).cards  # guess in order
    random.shuffle(target_list)  # shuffle tgt list

    sames = 0
    indexes_found = []
    current_guess_index = 0
    for i in range(len(target_list)):  # cycle through target cards and guess top card from guess
        target_card = target_list[i]
        total_len = 0
        guess = guess_list[current_guess_index]
        while current_guess_index in indexes_found:
            guess = guess_list[current_guess_index]
            current_guess_index += 1

        if target_card == guess:
            sames += 1

        loc_of_true = -1
        while True:
            loc_of_true = guess_list.index(target_list[i], loc_of_true + 1)
            if loc_of_true not in indexes_found:
                indexes_found.append(loc_of_true)
                break

        # print("Guess number: " + str(i) + " guess: " + str(guess) + " target card: " + str(target_card) + ". guess is at position " + str(loc_of_true))

    amount_correct.append(sames)
    total += sames

df = pd.DataFrame(amount_correct)

n_bins = 20
n, bins, patches = plt.hist(x, n_bins)

# Generate a normal distribution, center at x=0 and y=5
num_bins = 5
n, bins, patches = plt.hist(amount_correct, num_bins)


plt.show()


print(df.describe())
print(total*1.0/iters)

