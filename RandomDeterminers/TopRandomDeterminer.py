import numpy as np
from ARandomDeterminer import ARandomDeterminer


class TopRandomDeterminer(ARandomDeterminer):

    def make_guesses(self, target_list: np.array, shuffle: int = 0) -> int:
        ## takes in tgt deck and guess deck and see how many we get right
        sames = 0
        indexes_found = []
        current_guess_index = 0
        guess_list = np.arange(len(target_list))
        for i in range(len(target_list)):  # cycle through target cards and guess top card from guess
            target_card = target_list[i]
            while current_guess_index in indexes_found:
                current_guess_index += 1

            guess = guess_list[current_guess_index]
            if target_card == guess:
                sames += 1

            loc_of_true = -1
            while True: ## handling for multiple decks
                all_locs = np.where(guess_list == target_list[i])
                loc_of_true = np.where(all_locs[0] > loc_of_true, all_locs, all_locs)[0]
                ## get first location where we havent yet seen it
                if loc_of_true not in indexes_found:
                    indexes_found.append(loc_of_true)
                    break

        return sames

    def get_title(self):
        return "Select top card on random deck"

    def get_name(self):
        return "Top"