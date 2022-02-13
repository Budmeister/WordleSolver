from matplotlib import pyplot as plt

max_tries = 13

bbh_results = [0] * max_tries
bbh_sum = 0
bbh_count = 0
with open("output/wordle_output_part3.txt", "r") as file:
    for line in file.readlines():
        result = eval(line[:-1])
        bbh_results[result[0]] += 1
        bbh_sum += result[0]
        bbh_count += 1

b_results = [0] * max_tries
b_sum = 0
b_count = 0
with open("output/wordle_output2.txt", "r") as file:
    for line in file.readlines():
        result = eval(line[:-1])
        b_results[result[0]] += 1
        b_sum += result[0]
        b_count += 1

print(bbh_sum / bbh_count)
print(b_sum / b_count)

fig = plt.figure()
plt.xlabel("xlabel")
plt.ylabel("ylabel")
# ax = fig.add_axes([0,0,1,1])
plt.bar(list(range(max_tries)), bbh_results, width=0.4)
plt.bar([x + 0.4 for x in range(max_tries)], b_results, width=0.4)
plt.show()
