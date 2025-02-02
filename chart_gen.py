import os, csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 22})

labels, data = [], []
with os.scandir() as entries:
    for entry in entries:
        if ".csv" in entry.name:
            with open(entry.name, "r", newline="") as csv_file:
                labels.append(entry.name)
                data.append(list(csv.reader(csv_file)))

bot = labels[0].split("_")[-1].split(".")[0].split("-")[0]
labels = [l.split("_")[-1].split(".")[0].split("-")[1] for l in labels]

ml_wins = [len(d) for d in data]
ml_lost = [int(d[-1][0]) - win for d, win in zip(data, ml_wins)]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, ml_wins, width, label='{} Wins'.format(bot), color="#ffb600")
rects2 = ax.bar(x + width/2, ml_lost, width, label='{} Lost'.format(bot), color="#cc1c02")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of games')
ax.set_title('{} wins and losses against various bots in 1000 games'.format(bot))
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()
