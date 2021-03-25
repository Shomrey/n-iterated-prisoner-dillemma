from random_prisoner import RandomPrisoner
import numpy as np

class NIPRGame:

  def __init__(self, player_count):
    self.prisoners = [RandomPrisoner(i, p)
                      for i, p in zip(range(player_count), np.linspace(0, 1, player_count))]
    self.rounds = 0

  def get_payoffs(self, actions):
    cooperators = actions.count("C")
    payoffs = []
    for action in actions:
      if action == "C": # Cooperated
        payoffs.append((cooperators - 1) * 2)
      else: # Defected
        payoffs.append(cooperators * 2 + 1)
    return payoffs

  def simulate_round(self):
    actions = [p.choose_action() for p in self.prisoners]
    payoffs = tuple(self.get_payoffs(actions))
    for prisoner, payoff in zip(self.prisoners, payoffs):
      prisoner.receive_payoff(payoff)
      prisoner.update(actions)
    self.rounds += 1

  def simulate_rounds(self, rounds):
    for _ in range(rounds):
      self.simulate_round()

  def average_payoffs(self):
    return [p.total_payoff / self.rounds for p in self.prisoners]


def main():
  game = NIPRGame(10)
  game.simulate_rounds(100000)
  print(game.average_payoffs())

if __name__ == "__main__":
  main()
