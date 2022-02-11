# WordleSolver

This is my best shot at a Wordle bot. I have three methods; the first, brians method, is very intuitive and efficient--`O(Ta)`. The second is a combination of the brians method and a much less efficient, brute force method--`O(La^2 * Ta)`. The final method, the partition method, is the best and functions by partitioning the list of possible words, `La`, and choosing the guess which will give the smallest partitions. I developed the partition method before I watched <a href="https://youtu.be/v68zYyaEmEA">3b1b's video</a>, but I realize that it is exactly the same (as far as I can tell) except that I evaluate partitions by length rather than by bits.

`WordleDictionaries.py` contains two lists, `La`, (2315) and `Ta`, (10657), which are word dictionaries pulled from the official Wordle website on February 2, 2022. `La` is the list of words eligable to be the key. `Ta` is the list of other words which are valid guesses even though they are obscure enough to never be the key. The words of `Ta` can be very useful guesses for getting information.

In the algorithm descriptions, to keep it simpler, I will refer to `La` as the list of words which could be the key at any given moment and `Ta` as the list of possible guesses, that is, `La + Ta`.

## The Algorithms

All algorithms are modeled around a system where a word is submitted (`offer()`), and a result is used to narrow down `La`. Then a new guess is submitted, and `La` is reduced again. 

### brians method (`WordleSolverA.py`)

On each iteration (turn), brians method creates a list of letter frequencies by counting the number of times each letter occurs in `La`. Then, it gives each word in `Ta` a score which is the sum of the frequencies of the letters in that word, barring duplicate letters. (e.g. `'skill'` would only get a score boost for one of it's 'l's. The other is not likely to give any more information.) The score is also not boosted if that letter has had a response of yellow in the past (that information is already known). The word with the highest score is chosen.

### Brute Force (bf) (`WordleSolverB.py`)

The brute force method loops through every word in `Ta` and assigns it a score. The score is determined by the number of words that would be remaining in `La` if that word were the next guess. Since the key is not yet known, it takes the average new length of `La` across all possible keys in `La`. Because of this, the method is quite slow, `O(La^2 * Ta)`. There is a possible time optimization for it, and that is what the partition method was intended to be. However, the partition method also became much more efficient, winning Wordle in fewer guesses. This indicates that there are significant problems with brians method and the brute force method. 

### Partition Method (`WordleSolverC.py`)

The partition method aims to be as close to "perfect" as possible. After a guess is submitted and a response is received, `La` is partitioned into sub-dictionaries. All the keys in each subdictionary would give the same response given a specific guess. Then, to process the real response, `La` is reduced to the partition which corresponds to the response. A guess is selected according to the expected average partition length. That is, for every guess in `Ta`, `La` is partitioned, and the length of the partitions is averaged with a weighted average, the weights being the probablility of each partition containing the real key--which is the same as the length of the partition. The full expression becomes 

```score = sum([len(partition[key]) ** 2 for key in partition]) / total_words```. 
