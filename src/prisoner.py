class Prisoner:

  def __init__(self, index):
    self.index = index
    self.total_payoff = 0

  # Return the action chosen for next round
  def choose_action(self):
    raise NotImplementedError

  # Called after a round was concluded
  def receive_payoff(self, payoff):
    self.total_payoff += payoff

  # Called after a round was concluded with array of actions taken by all prisoners
  def update(self, actions):
    pass
