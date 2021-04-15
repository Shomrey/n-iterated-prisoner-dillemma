class Strategy:
  """
  A prisoner factory. Can create a prisoner with given id and has a display name
  """

  def __init__(self, factory, name):
    self.factory = factory
    self.name = name

  # important that id is unique in whole game!
  def make_prisoner(self, id):
    return self.factory(id)

  def get_name(self):
    return self.name
