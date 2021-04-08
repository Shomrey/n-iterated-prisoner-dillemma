from nipd import NIPDGame
from random_prisoner import RandomPrisoner
import numpy as np
import matplotlib.pyplot as plt

class Tournament:

  def __init__(self, strategies, rounds, round_player_count):
    """
    Creates a new round-robin tournament.

    Parameters:
     strategies: array of participating strategies
     rounds: number of rounds to play in each match
     round_player_count: number of duplicated representatives of each strategy in matches
    """

    self.participants = [Participant(strategy) for strategy in strategies]
    self.rounds = rounds
    self.round_player_count = round_player_count

  def run(self):
    self.result_matrix = {}
    for i in range(len(self.participants)):
      for j in range(i, len(self.participants)):
        self.run_round(self.participants[i], self.participants[j])

  def run_round(self, part_a, part_b):
    prisoners_a = [part_a.strategy.make_prisoner(i) for i in range(self.round_player_count)]
    prisoners_b = [part_b.strategy.make_prisoner(i + self.round_player_count) for i in range(self.round_player_count)]

    game = NIPDGame(prisoners_a + prisoners_b)
    game.simulate_rounds(self.rounds)

    average_payoffs = game.average_payoffs()
    self.result_matrix[(part_a, part_b)] = np.mean([average_payoffs[p.id] for p in prisoners_a])
    self.result_matrix[(part_b, part_a)] = np.mean([average_payoffs[p.id] for p in prisoners_b])

  def plot_result_matrix(self):
    matrix = np.array([[self.result_matrix[j, i]
                        for j in self.participants]
                       for i in self.participants])
    fig = plt.figure()
    ax = fig.add_subplot()
    cax = ax.matshow(matrix)
    fig.colorbar(cax)

    ax.set_xlabel("player")
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("opponent")
    ax.set_xticklabels([''] + [p.strategy.name for p in self.participants], rotation="vertical")
    ax.set_yticklabels([''] + [p.strategy.name for p in self.participants])
    fig.tight_layout()

    plt.show()


class Participant:

  def __init__(self, strategy):
    self.strategy = strategy

if __name__ == "__main__":
  t = Tournament([RandomPrisoner.strategy(p) for p in np.linspace(0, 1, 5)], 1000, 4)
  t.run()
  t.plot_result_matrix()
