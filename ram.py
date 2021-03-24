# Helps to interface with ram np arrays

class Ram(object):
  def __init__(self, data):
    self._data = data
  
  def uint8_at_addr(self, addr):
    return self._data[addr]