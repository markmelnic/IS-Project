from argparse import ArgumentParser
from api import State, util, engine
import random, time, csv, os

def run_tournament(options):

    botnames = options.players.split(",")
    print(botnames)

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    print('Playing {} games:'.format(int(totalgames)))

    #if not os.find("T_Dataset.csv"):
    with open("T_Dataset_{}.csv".format(botnames[options.indexed - 1]), "a", newline="") as t_data:
        t_writer = csv.writer(t_data)

        for a, b in matches:
            for r in range(options.repeats):

                if random.choice([True, False]):
                    p = [a, b]
                else:
                    p = [b, a]

                # Generate a state with a random seed
                seed = random.randint(1000000, 9999999)
                state = State.generate(id=seed, phase=int(options.phase))

                winner, score = engine.play(bots[p[0]], bots[p[1]], state, options.max_time*1000, verbose=options.verbose, fast=options.fast)

                if winner is not None:
                    winner = p[winner - 1]
                    wins[winner] += score

                    if winner == options.indexed - 1:
                        t_writer.writerow([seed])

                playedgames += 1
                print('Played {} out of {:.0f} games ({:.0f}%): {}, seed {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins, seed))

    print('Results:')
    for i in range(len(bots)):
        games_won = int(wins[i] / 100000) + int(wins[i] % 100000)
        print('    bot {}: {} points, won {} games'.format(bots[i], wins[i], games_won))


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-s", "--starting-phase",
                        dest="phase",
                        help="Which phase the game should start at.",
                        default=1)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    parser.add_argument("-f", "--fast",
                        dest="fast",
                        action="store_true",
                        help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="Print verbose information")

    parser.add_argument("-i", "--indexed",
                        dest="indexed",
                        help="Chose the wins of which player should be tracked (player 1 / 2)",
                        type=int, default=1)

    run_tournament(parser.parse_args())
