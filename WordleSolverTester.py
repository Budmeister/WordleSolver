from WordleDictionaries import *

    
def offer(word, key):
    return [
        'g' if key[i] == word[i] else
        'y' if word[i] in key else 'r'
        for i in range(len(key))
    ]

def possible_given_result(word_to_check, word_checked, result):
    for i, r in enumerate(result):
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

words = La + Ta

possible_words = ['waste', 'paste', 'caste', 'haste', 'taste', 'baste']
# key = 'taste'
scores = [[0, word] for word in words]

for key in possible_words:

    best_words = []

    for i, word in enumerate(words):
        result = offer(word, key)
        new_possible_words = list(filter(lambda x: possible_given_result(x, word, result), possible_words))
        scores[i][0] += len(new_possible_words)
        if len(new_possible_words) == 1:
            best_words.append((word, new_possible_words))
            scores[i].append(new_possible_words)

scores.sort()
print(scores[:100])
print()
