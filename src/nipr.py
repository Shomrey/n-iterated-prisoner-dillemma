from random_prisoner import RandomPrisoner
import numpy as np

class NIPRGame:

  def __init__(self, player_count):
    self.prisoners = [RandomPrisoner(i, p)
                      for i, p in zip(range(player_count), np.linspace(0, 1, player_count))]
    self.rounds = 0

  def get_payoffs(self, actions):
    cooperators = list(actions.values()).count("C")
    payoffs = {}
    for prisoner in self.prisoners:
      payoff = self.get_payoff(actions[prisoner.id], cooperators)
      payoffs[prisoner.id] = payoff
    return payoffs

  def get_payoff(self, action, cooperators):
    if action == "C":
      return (cooperators - 1) * 2
    else:
      return cooperators * 2 + 1

  def simulate_round(self):
    actions = { p.id: p.choose_action()
                for p in self.prisoners }
    payoffs = self.get_payoffs(actions)
    for prisoner in self.prisoners:
      prisoner.receive_payoff(payoffs[prisoner.id])
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
