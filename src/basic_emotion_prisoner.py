from prisoner import Prisoner
from strategy import Strategy

class BasicEmotionPrisoner(Prisoner):
    prisoner_type = 'basic_emotion'

    def __init__(self, id, emotion_multiplier):
        super().__init__(id)
        self._prisoner_type = BasicEmotionPrisoner.prisoner_type
        self._emotion_multiplier = emotion_multiplier
        self._emotion = 1.0
        # above 0.5 -> C
        # below 0.5 -> D
        self._decision_threshold = 0.5

    def strategy(emotion_multiplier):
        return Strategy(lambda id: BasicEmotionPrisoner(id, emotion_multiplier), BasicEmotionPrisoner.prisoner_type)

    def choose_action(self):
        #print(self._emotion)
        #print('C' if self._emotion > self._decision_threshold else 'D')
        return 'C' if self._emotion > self._decision_threshold else 'D'

    def get_type(self):
        return self._prisoner_type

    def update(self, actions):
        C = 0.0
        D = 0.0
        number_of_players = 0.0
        for player in actions:
            if player == self.id:
                continue

            if actions[player] == 'C':
                C += 1
            else:
                D += 1
            number_of_players += 1

        self._emotion += (((C-D)/number_of_players) * self._emotion_multiplier)
