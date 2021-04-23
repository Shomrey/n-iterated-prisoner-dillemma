from prisoner import Prisoner
from strategy import Strategy

class CopyPrisoner(Prisoner):
    prisoner_type = 'copy_previous'

    def __init__(self, id):
        super().__init__(id)
        self._prisoner_type = CopyPrisoner.prisoner_type
        self._next_vote = 'C'

    def strategy(empty = 0):
        return Strategy(lambda id: CopyPrisoner(id), CopyPrisoner.prisoner_type)

    def choose_action(self):
        return self._next_vote

    def get_type(self):
        return self._prisoner_type

    def update(self, actions):
        C = 0
        D = 0
        for action in actions:
            if actions[action] == 'C':
                C += 1
            else:
                D += 1
        self._next_vote = 'C' if C >= D else 'D'