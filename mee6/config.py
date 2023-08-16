class Economy:
  def __init__(self):
    self.interval = 3600
    self.interval_variation = [0, 600]
    self.messages = ['!work claim', '!work']
    self.messages_variation = [5, 15]

class Counting:
  def __init__(self):
    self.interval = 120
    self.interval_variation = [-10, 60]
    self.probability = 0.7

class Hours:
  def __init__(self):
    self.hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21]
    self.hours_variation = [0, 3600]

class Config:
  def __init__(self):
    self.economy = Economy()
    self.counting = Counting()
    self.hours = Hours()
