from matplotlib import pyplot as plt


bbh_results = [0] * 8
bbh_sum = 0
bbh_count = 0
with open("output/wordle_output_part1.txt", "r") as file:
    for line in file.readlines():
        result = eval(line[:-1])
        bbh_results[result[0]] += 1
        bbh_sum += result[0]
        bbh_count += 1

b_results = [0] * 8
b_sum = 0
b_count = 0
with open("output/wordle_output_bf.txt", "r") as file:
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
plt.bar(list(range(8)), bbh_results, width=0.4)
plt.bar([x + 0.4 for x in range(8)], b_results, width=0.4)
plt.show()
