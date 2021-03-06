
from WordleDictionaries import *
from math import sqrt

words = La + Ta
print(words[:20])
print(len(words))

def let(letter):
    return ord(letter) - ord('a')

class SolverC:

    def __init__(self):
        self.first_word = 'roate'

    
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
                if mod_key[j] != '*' and mod_key[i] != '*':
                    result[i] = 'y'
                    mod_key[j] = '*'
            except ValueError:
                pass
        return result
        
    
    def offer_unknown_key(self, word):
        print(word)
        return list(input().strip())

    def solve(self, key='*****', verbose=True, key_known=True):
        self.verbose = verbose
    
        self.possible_words = La.copy()
    
        guess_num = 0
        result = []
        prev_guess_score = -2
        prev_guess = ""
        while result != ['g'] * len(key):
            g = self.get_guess()
            s = g[0]
            guess = g[1]
            part = g[2] if len(g) == 3 else None
            if verbose:
                print((guess_num, s, guess, len(self.possible_words) if len(self.possible_words) > 10 else self.possible_words))
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
            if part:
                self.process_result(result, part)
            else:
                self.possible_words = [x for x in self.possible_words if self.offer(guess, x) == result]
            prev_guess_score = s
            prev_guess = guess
            guess_num += 1

    def process_result(self, result, part):
        self.possible_words = part[tuple(result)]

    def get_guess(self):
        if len(self.possible_words) == len(La):
            return 0, self.first_word
        elif len(self.possible_words) == 2:
            return 0, self.possible_words[0]
        elif len(self.possible_words) == 1:
            return -1, self.possible_words[0]
        elif len(self.possible_words) == 0:
            if self.verbose:
                print("No more possible words!")
            return -1, '*****'
        
        
        scores = self.part_method(words, self.possible_words)
        return min(scores)

    def partition(self, guess, keys):
        parts = {}
        for key in keys:
            result = self.offer(guess, key)
            result = tuple(result)
            part = []
            if result in parts:
                part = parts[result]
            else:
                parts[result] = part
            part.append(key)
        return parts

    def avg_partition_len(self, partition, total_words):
        return sum([len(partition[key]) ** 2 for key in partition]) / total_words

    def part_method(self, words_to_check, keys):
        scores = []
        for guess in words_to_check:
            parts = self.partition(guess, keys)
            score = self.avg_partition_len(parts, len(keys))
            scores.append((score, guess, parts))
        return scores
        
                


if __name__ == "__main__":
    from tqdm import tqdm
    endings = [0, 0, 0]
    avg_tries = 0

    results = []

    s = SolverC()

    num_words = 0
    for i, word in tqdm(enumerate(La), total=len(La)):
        num_tries, ending = s.solve(word, verbose=False)
        avg_tries += num_tries
        endings[ending] += 1
        results.append((num_tries, ending, word))
        num_words += 1

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

    with open("output/wordle_output_part3.txt", "w") as file:
        file.writelines([str(result) + "\n" for result in results])

