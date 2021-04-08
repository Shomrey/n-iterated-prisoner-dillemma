class Strategy:
  """
  A prisoner factory. Can create a prisoner with given id and has a display name
  """

  def __init__(self, factory, name):
    self.factory = factory
    self.name = name

  def make_prisoner(self, id):
    return self.factory(id)
