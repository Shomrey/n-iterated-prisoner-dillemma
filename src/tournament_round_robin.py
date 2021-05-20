from nipd import NIPDGame
from random_prisoner import RandomPrisoner
from basic_emotion_prisoner import BasicEmotionPrisoner
from copy_prisoner import CopyPrisoner
from qlearning_prisoner import QLearningPrisoner
import numpy as np
import matplotlib.pyplot as plt
from participant import Participant

class Tournament_round_robin:

  def __init__(self, strategies, rounds, round_player_count):
    """
    Creates a new round-robin tournament.

    Parameters:
     strategies: array of participating strategies
     rounds: number of rounds to play in each match
     round_player_count: number of duplicated representatives of each strategy in matches

    Fields:
     result_matrix: dictionary where key is pair of participants and value is average_payoff of the first in match
    """

    self._participants = [Participant(strategy) for strategy in strategies]
    self._rounds = rounds
    self._round_player_count = round_player_count
    self._result_matrix = {}


  def run(self):
    #clear possible previous results
    self._result_matrix = {}
    for i in range(len(self._participants)):
      for j in range(i, len(self._participants)):
        self.run_round(self._participants[i], self._participants[j])

  def run_round(self, part_a, part_b):
    prisoners_a = [part_a.strategy.make_prisoner(i) for i in range(self._round_player_count)]
    prisoners_b = [part_b.strategy.make_prisoner(i + self._round_player_count) for i in range(self._round_player_count)]

    game = NIPDGame(prisoners_a + prisoners_b)
    game.simulate_rounds(self._rounds)

    average_payoffs = game.average_payoffs()
    self._result_matrix[(part_a, part_b)] = np.mean([average_payoffs[p.id] for p in prisoners_a])
    self._result_matrix[(part_b, part_a)] = np.mean([average_payoffs[p.id] for p in prisoners_b])

  def get_results_raw(self):
    return self._result_matrix

  def plot_result_matrix(self):
    matrix = np.array([[self._result_matrix[j, i]
                        for j in self._participants]
                       for i in self._participants])
    fig = plt.figure()
    ax = fig.add_subplot()
    cax = ax.matshow(matrix)
    fig.colorbar(cax)

    ax.set_xlabel("player")
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("opponent")
    ax.set_xticklabels([''] + [p.strategy.name for p in self._participants], rotation="vertical")
    ax.set_yticklabels([''] + [p.strategy.name for p in self._participants])
    fig.tight_layout()

    plt.show()




if __name__ == "__main__":
  participants = [RandomPrisoner.strategy(p) for p in np.linspace(0, 1, 5)]
  #participants = []
  participants.append(RandomPrisoner.strategy(0.5))
  participants.append(QLearningPrisoner.strategy())
  t = Tournament_round_robin(participants, 1000, 1)
  t.run()
  #for result in t.get_results_raw():
    #print(result[0].strategy.get_name())
  t.plot_result_matrix()
