from prisoner import Prisoner
from strategy import Strategy
import numpy as np

class QLearningEmotionPrisoner(Prisoner):
    prisoner_type = 'q-learning-emotion'

    def __init__(self, id):
        super().__init__(id)
        self._prisoner_type = QLearningEmotionPrisoner.prisoner_type
        self._last_payoff = 0
        self._next_vote = 'C'
        self._qlearning_model = QLearningModel()

    def strategy(empty = 0):
        return Strategy(lambda id: QLearningEmotionPrisoner(id), QLearningEmotionPrisoner.prisoner_type)

    def choose_action(self):
        return self._next_vote

    def get_type(self):
        return self._prisoner_type

    #override from Prisoner class
    def receive_payoff(self, payoff):
        self._last_payoff = payoff
        self.total_payoff += payoff

    def update(self, actions):
        self._next_vote = self._qlearning_model.run_round(actions, self._next_vote, self._last_payoff)

class QLearningModel():
    def __init__(self, learning_rate=0.9, reward_discount=0.9, epsilon=0.9, emotion_multiplier=0.5):
        # enemy_play_C action_C
        # enemy_play_D action_D
        self._qtable = np.zeros((2,2))
        self._learning_rate = learning_rate
        self._reward_discount = reward_discount
        self._epsilon = epsilon
        # state is defined as what play in the last round the enemy did
        self._current_state_idx = 0
        self._move_dict = {'C': 0, 'D': 1}
        self._performed_actions = []
        self._emotion_multiplier = emotion_multiplier
        self._emotion = 1.0
        self._break_point = 0.5 # above 0.5 - C    below 0.5 - D
        # TODO find a better way to show results
        self._show_tick = 0

    def get_move_idx(self, move_str):
        return self._move_dict[move_str]

    def get_move_str(self, move_idx):
        rev_move_dict = {v: k for k, v in self._move_dict.items()}
        return rev_move_dict[move_idx]

    def calculate_state(self):
        return 'C' if self._emotion > 0.5 else 'D'

    def update_emotion(self, actions):
        C = 0.0
        D = 0.0
        number_of_players = 0.0
        for action in actions:
            if actions[action] == 'C':
                C += 1
            else:
                D += 1
            number_of_players += 1
        self._emotion += (((C - D) / number_of_players) * self._emotion_multiplier)

    def run_round(self, actions, last_action, round_payoff):
        state = self._current_state_idx
        last_action_idx = self.get_move_idx(last_action)
        # update q-table
        old_q_value = self._qtable[state][last_action_idx]
        learning_difference = round_payoff + self._reward_discount * np.max(self._qtable[state]) - old_q_value
        new_q_value = old_q_value + learning_difference * self._learning_rate
        # change state
        self.update_emotion(actions)
        self._qtable[state][last_action_idx] = new_q_value
        self._current_state_idx = self.get_move_idx(self.calculate_state())
        # choose next action
        epsilon_random_val = np.random.random()
        if self._show_tick == 999:
            print(self._qtable)
            print(self._performed_actions)
        else:
            self._show_tick += 1
        if epsilon_random_val < self._epsilon:
            idx = np.argmax(self._qtable[self._current_state_idx])
            move = self.get_move_str(idx)
            self._performed_actions.append(move)
            return move
        else:
            move = self.get_move_str(np.random.randint(self._qtable.shape[0]))
            self._performed_actions.append(move)
            return move




