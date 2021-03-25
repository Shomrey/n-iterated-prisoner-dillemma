from prisoner import Prisoner

from random import random

class RandomPrisoner(Prisoner):

  def __init__(self, index, cooperation_chance):
    super().__init__(index)
    self.cooperation_chance = cooperation_chance

  def choose_action(self):
    return 'C' if random() <= self.cooperation_chance else 'D'
