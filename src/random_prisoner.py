from prisoner import Prisoner
from strategy import Strategy

from random import random

class RandomPrisoner(Prisoner):
  prisoner_type = 'random_{}'

  def __init__(self, id, cooperation_chance):
    super().__init__(id)
    self.cooperation_chance = cooperation_chance
    self._prisoner_type = RandomPrisoner.prisoner_type.format(cooperation_chance)

  def strategy(cooperation_chance):
    return Strategy(lambda id: RandomPrisoner(id, cooperation_chance),
                    RandomPrisoner.prisoner_type.format(cooperation_chance))

  def choose_action(self):
    random_val = random()
    return 'C' if  random_val <= self.cooperation_chance else 'D'

  def get_type(self):
    return self._prisoner_type
