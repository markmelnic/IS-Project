import os, csv
from scipy.stats import binom_test
from rich import print
from rich.table import Table

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

tab = Table(header_style="bold magenta", title=bot.upper()+" bot one-tailed binomial test")
tab.add_column("Opponent")
tab.add_column("Probability")

for lb, mw, ml in zip(labels, ml_wins, ml_lost):
    bres = 1 - binom_test(mw, n=mw+ml, p=0.5, alternative='greater')
    tab.add_row(lb, str(bres))

print("\n", tab, "\n")
