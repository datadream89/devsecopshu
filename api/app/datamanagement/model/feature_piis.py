from datamanagement.model.feature_pii import Flare
class FeaturePiis(object):
  def __init__(self, name, piis=None):
    self.name = name
    self.piis = piis

  def to_flare(self):
    d = Flare(self.name, self.piis)
    return d



