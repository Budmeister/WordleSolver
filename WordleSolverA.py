import random
from WordleDictionaries import *

words = []

# with open("sgb-words.txt", "r") as file:
with open("LaTa.txt", "r") as file:
    words = [line[:-1] for line in file.readlines()]
print(words[:20])
print(len(words))

def let(letter):
    return ord(letter) - ord('a')

class SolverA:

    def get_freqs(self, dictionary):
        f = [0] * 26
        for word in dictionary:
            for letter in word:
                f[let(letter)] += 1
        return f
    
    def offer(self, word, key):
        mod_key = list(key)
        result = ['r'] * len(key)
        for i in range(len(key)):
            if key[i] == word[i]:
                result[i] = 'g'
                mod_key[i] = '*'
        for i in range(len(key)):
            try:
                j = mod_key.index(word[i])
                if word[i] in mod_key:
                    result[i] = 'y'
                    mod_key[j] = '*'
            except ValueError:
                pass
        return result
    
    def offer_unknown_key(self, word, key):
        print(word)
        return input()

    def possible_given_result(self, word_to_check, word_checked, result):
        for i, r in enumerate(result):
            if self.greens[i] != '*' and self.greens[i] != word_to_check[i]:
                return False
            if r == 'r':
                if word_checked[i] in word_to_check:
                    return False
            elif r == 'y':
                if word_checked[i] == word_to_check[i]:
                    return False
            elif r == 'g':
                if word_checked[i] != word_to_check[i]:
                    return False
        return True

    def solve(self, key, verbose=True, key_known=True):
        if not key_known:
            self.offer = self.offer_unknown_key
        self.verbose = verbose
        self.freqs = self.get_freqs(words)
    
        # self.possible_words = words.copy()
        self.possible_words = La.copy()
        self.knowledge = [['*'] * len(key) for _ in range(26)]
        self.yellows = []    # (letter, info)
        self.greens = ['*'] * len(key)
    
        guess_num = 0
        result = []
        prev_guess_score = -2
        prev_guess = ""
        while result != ['g'] * len(key):
            s, guess = self.get_guess()
            if verbose:
                print((guess_num, s, guess, "".join(self.greens), [yellow[0] + ": " + "".join(yellow[1]) for yellow in self.yellows], len(self.possible_words) if len(self.possible_words) > 10 else self.possible_words))
            if guess == key:
                if verbose:
                    print("Correct!")
                return guess_num+1, 0
            if s == -1:
                if verbose:
                    print("Final guess")
                return guess_num+1, 1
            if s == prev_guess_score and guess == prev_guess:
                if verbose:
                    print("Same guess score twice")
                return guess_num+1, 2
            result = self.offer(guess, key)
            self.process_result(guess, result, key)
            prev_guess_score = s
            prev_guess = guess
            guess_num += 1

    def proc_green(self, i, letter, key):
        if (letter, self.knowledge[let(letter)]) in self.yellows:
            self.yellows.remove((letter, self.knowledge[let(letter)]))
        self.knowledge[let(letter)] = i
        self.greens[i] = letter

    def proc_yellow(self, i, letter, key):
        if not isinstance(self.knowledge[let(letter)], list):
            return
        self.knowledge[let(letter)][i] = 'y'
        if (letter, self.knowledge[let(letter)]) not in self.yellows:
            self.yellows.append((letter, self.knowledge[let(letter)]))

        # check if all but one are yellow (also checked at the end)
        guess = -1
        for pos in range(len(key)):
            if self.knowledge[let(letter)][pos] != 'y':
                if guess == -1:
                    guess = pos
                else:
                    guess = -2
                    break
        if guess != -2:
            self.knowledge[let(letter)][guess] = 'g'
            self.proc_green(guess, letter, key)

    def proc_red(self, i, letter, key):
        self.knowledge[let(letter)] = False

    def process_result(self, word, result, key):
        for i, letter in enumerate(word):
            if result[i] == 'g':
                self.proc_green(i, letter, key)
            elif result[i] == 'y':
                self.proc_yellow(i, letter, key)
            elif result[i] == 'r':
                self.proc_red(i, letter, key)

        for yellow in self.yellows:
            for i, letter in enumerate(self.greens):
                if letter != "*":
                    yellow[1][i] = 'y'
            guess = -1
            for i, letter in enumerate(yellow[1]):
                if letter != 'y':
                    if guess == -1:
                        guess = i
                    else:
                        guess = -2
                        break
            if guess != -2:
                yellow[1][guess] = 'g'
                self.proc_green(guess, yellow[0], key)
        
        self.possible_words = list(filter(lambda x: self.possible_given_result(x, word, result), self.possible_words))
        self.freqs = self.get_freqs(self.possible_words)

    def get_guess(self):
        if '*' not in self.greens:
            return -1, "".join(self.greens)
        if len(self.possible_words) == 1:
            return -1, self.possible_words[0]
        elif len(self.possible_words) == 0:
            if self.verbose:
                print("No more possible words!")
        
        potential_guesses = []

        for word in words:
            s = 0
            for i, letter in enumerate(word):
                if self.knowledge[let(letter)] and not isinstance(self.knowledge[let(letter)], int) and self.knowledge[let(letter)][i] != 'y':
                    if (letter, self.knowledge[let(letter)][i]) in self.yellows and self.knowledge[let(letter)][i] != 'y':
                        s += self.freqs[let(letter)]
                    elif letter not in word[:i]:
                        s += self.freqs[let(letter)]
            if len(self.possible_words) <= 10 and word in self.possible_words:
                s += 0.5
            potential_guesses.append((s, word))
        
        # potential_guesses.sort()

        # return potential_guesses[-1]
        best_guess = potential_guesses[0]
        for guess in potential_guesses:
            if guess[0] > best_guess[0]:
                best_guess = guess
        return best_guess


if __name__ == "__main__":
    endings = [0, 0, 0]
    avg_tries = 0

    results = []

    s = SolverA()

    num_words = 0
    # for i, word in enumerate(words):
    for i, word in enumerate(La):
        num_tries, ending = s.solve(word, verbose=False)
        avg_tries += num_tries
        endings[ending] += 1
        results.append((num_tries, ending, word))
        num_words += 1
        if i % 100 == 0:
            print('{0:.{1}f}%'.format(i / len(La) * 100, 3))

    results.sort()
    avg_tries /= num_words

    print("Results are in!")
    print(results[:20])
    print()
    print(results[-20:])
    print()

    print("The average length of game was: ", avg_tries)
    print(endings[0], " words were guessed correctly.")
    print(endings[1], " words were guessed incorrectly.")
    print(endings[2], " words were never guessed.")

    with open("wordle_output.txt", "w") as file:
        file.writelines([str(result) + "\n" for result in results])

