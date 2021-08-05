import collections
from typing import Dict, List

import requests
import pyrebase
from datamanagement.configuration.key import FIREBASE_CONFIG

RULES_TABLE = 'rules'
REGEX_TABLE = 'regexes'




class Rules(collections.OrderedDict):
  list_to_tuple = lambda x: {False: x, True: tuple(x)}.get(isinstance(x, list), ' ')#if of type list convert it first to tuple
  ensure_set = lambda x: {False: set(x), True: x}.get(isinstance(x, set), ' ')

  def __init__(self, **kwargs):
    super().__init__(self, **kwargs)

  def add(self, other):
    for key in self:
      if key in other:
        self[key] = list(Rules.ensure_set(self[key]) | Rules.ensure_set(other[key]))
      else:
        pass

  def removed_from(self, other):
    for key in self:
      if key in other:
        self[key] =  list(Rules.ensure_set(other[key]) - Rules.ensure_set(self[key]))
      else:
        pass


class dbHandler():

  def __init__(self) -> None:
    self._dbHandle = self.firebase_db_init()

  def firebase_db_init(self) -> None:
    try:
      firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
      return firebase.database()
    except Exception as e:
      print("db_init failed. {}".format(e))

  def get_url(self, url):
    r = requests.get(url)
    if r.status_code == 200:
      return r.json()
    else:
      print("HTTP GET {} failed with status={}".format(url, r.status_code))

  def add_rules(self, tableName: str, keyName: str, data: Rules) -> None:
    data_exists = self.get_record(tableName, keyName)

    if data_exists:
     data.add(data_exists)

    try:
      self._dbHandle.child(tableName).child(keyName).set(data)
    except Exception as e:
      print("set_record failed. {}".format(e))

  def remove_rules(self, tableName: str, keyName: str, data: Rules) -> None:
    data_exists = self.get_record(tableName, keyName)

    if data_exists:
     data.removed_from(data_exists)

    try:
      self._dbHandle.child(tableName).child(keyName).set(data)
    except Exception as e:
      print("set_record failed. {}".format(e))

  def get_record(self, tableName: str, keyName: str) -> Dict:
    try:
      return self._dbHandle.child(tableName).child(keyName).get().val() or dict()
    except Exception as e:
      print("get_record failed. {}".format(e))

  def delete_record(self, tableName: str, keyName: str) -> None:
    try:
      self._dbHandle.child(tableName).child(keyName).remove()
    except Exception as e:
      print("delete_record failed. {}".format(e))

  def get_table_childs(self, tableName: str):
    try:
      pyres = self._dbHandle.child(tableName).get().pyres
      return pyres
    except Exception as e:
      print("Can't get the pyres for the table {}".format(e))

