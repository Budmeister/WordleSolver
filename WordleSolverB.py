
from WordleDictionaries import *
import istarmap
from multiprocessing import Pool

# with open("LaTa.txt", "r") as file:
#     words = [line[:-1] for line in file.readlines()]
words = La + Ta
print(words[:20])
print(len(words))

def let(letter):
    return ord(letter) - ord('a')

class SolverB:

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
                if mod_key[j] != '*':
                    result[i] = 'y'
                    mod_key[j] = '*'
            except ValueError:
                pass
        return result
    
    def offer_unknown_key(self, word):
        print(word)
        return list(input().strip())

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

    def solve(self, key='*****', verbose=True, key_known=True):
        self.verbose = verbose
        self.freqs = self.get_freqs(words)
    
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
            result = self.offer(guess, key) if key_known else self.offer_unknown_key(guess)
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
        
        num_guesses = 50
        brian = self.brians_method(num_guesses)
        if len(self.possible_words) < 1000:
            words_to_check = [x[1] for x in brian]
            scores = self.brute_force(words_to_check)
            scores.sort()
            return scores[0]
        
        return brian[-1]

    
    def brians_method(self, num_guesses):
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
        
        best_guesses = []
        for guess in potential_guesses:
            if len(best_guesses) < num_guesses or len(best_guesses) == 0 or guess[0] > best_guesses[0][0]:
                best_guesses.append(guess)
                best_guesses.sort()
            if len(best_guesses) > num_guesses:
                best_guesses.pop(0)
        return best_guesses

    def bf_eval_key(self, words_to_check, key, scores, e=-1):
        for i, word in enumerate(words_to_check):
            result = self.offer(word, key)
            len_new_possible = 0
            for poss_word in self.possible_words:
                if self.possible_given_result(poss_word, word, result):
                    len_new_possible += 1
            scores[i][0] += len_new_possible
        self.bfm_count += 1

    def bf_eval_guess(self, keys, word):
        score = 0
        for i, key in enumerate(keys):
            result = self.offer(word, key)
            len_new_possible = 0
            for poss_word in self.possible_words:
                if self.possible_given_result(poss_word, word, result):
                    len_new_possible += 1
            score += len_new_possible
        return score, word

    
    def brute_force(self, words_to_check, verbose=False):
        scores = [[0, word] for word in words_to_check]
        self.bfm_count = 0
        for e, key in enumerate(self.possible_words):
            self.bf_eval_key(words_to_check, key, scores)
        return scores

    def brute_force_multiprocess(self, words_to_check, possible_keys=None, verbose=False, num_processes=5):
        import tqdm
        if possible_keys is None:
            possible_keys = self.possible_words
        scores = []
        with Pool(num_processes) as p:
            counter = p.istarmap(self.bf_eval_guess, [(possible_keys, word) for word in words_to_check], chunksize=1000)
            for score in tqdm.tqdm(counter, total=len(self.possible_words)):
                scores.append(score)
        return scores
        
                


if __name__ == "__main__":
    endings = [0, 0, 0]
    avg_tries = 0

    results = []

    s = SolverB()

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

