
from typing import Dict, List

class Children():
  def __init__(self, value=None) -> None:

    if isinstance(value, bool):
      self.name = str(value)
    else:
      self.name = "percentage (%)"
      self.value = value

class Flare():
  def __init__(self, name=None, children=None) -> None:
    self.name: str = name
    self.children = [children] if not isinstance(children, List) else children

class FeaturePii(object):
  def __init__(self, feat_name, is_pii, most_likely_pii_type, pii_types_and_scores):
    self.feat_name: str = feat_name
    self.is_pii: bool = is_pii
    self.most_likely_pii_type: Dict[str, float] = most_likely_pii_type
    self.pii_types_and_scores: Dict[str, float] = pii_types_and_scores

  def to_flare(self ):
    d = Flare(self.feat_name, [])

    def append_children(attr, value, acc: List):
      if isinstance(value, dict):
        acc_inner = []
        for k, v in value.items():
          append_children(k, v, acc_inner)
        acc.append(Flare(attr, acc_inner))
      else:
        acc.append(Flare(attr, Children(value)))

    for attr, value in self.__dict__.items():
      print(attr)
      if attr != 'feat_name':
        append_children(attr, value, d.children)

    return d





