from nipd import NIPDGame
from random_prisoner import RandomPrisoner
import numpy as np
import matplotlib.pyplot as plt
from participant import Participant

class Tournament_all_in_one:
    def __init__(self, strategies, rounds, round_player_count):
        """
        Creates a new round-robin tournament.

        Parameters:
         strategies: array of participating strategies
         rounds: number of rounds to play in each match
         round_player_count: number of duplicated representatives of each strategy in matches

        Fields:
         result_matrix: dictionary where key is participant and value is average_payoff of the participant
        """

        self._participants = [Participant(strategy) for strategy in strategies]
        self._rounds = rounds
        self._round_player_count = round_player_count
        self._result_matrix = {}

    def run(self):
        self._result_matrix = {}
        prisoners = []
        current_id = 0
        for participant in self._participants:
            for i in range(self._round_player_count):
                prisoners.append(participant.strategy.make_prisoner(current_id))
                current_id += 1

        game = NIPDGame(prisoners)
        game.simulate_rounds(self._rounds)

        average_payoffs = game.average_payoffs()
        for prisoner in prisoners:
            self._result_matrix[prisoner] = average_payoffs[prisoner.id]

    def get_results_raw(self):
        return self._result_matrix

    def get_winner_by_value(self):
        analyzis_results = list(self._result_matrix.values())
        max_value = max(analyzis_results)
        winners = []
        for participant in self._result_matrix:
            if self._result_matrix[participant] == max_value:
                winners.append(participant)
        winning_strategies = [winner.get_type() for winner in winners]
        winning_strategies = list(dict.fromkeys(winning_strategies))
        return winning_strategies

    def get_winner_by_mean(self):
        #TODO
        return 0

if __name__ == "__main__":
  t = Tournament_all_in_one([RandomPrisoner.strategy(p) for p in np.linspace(0, 1, 5)], 1000, 4)
  t.run()
  print(t.get_winner_by_value())
