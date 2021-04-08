from prisoner import Prisoner
from strategy import Strategy

from random import random

class RandomPrisoner(Prisoner):

  def __init__(self, id, cooperation_chance):
    super().__init__(id)
    self.cooperation_chance = cooperation_chance

  def strategy(cooperation_chance):
    return Strategy(lambda id: RandomPrisoner(id, cooperation_chance),
                    f"random_{cooperation_chance}")

  def choose_action(self):
    return 'C' if random() <= self.cooperation_chance else 'D'
