from typing import Dict, List
import pandas as pd
import numpy as np

from collections import namedtuple

from datamanagement.configuration import paths
from datamanagement.controllers.data_driver import DataDriver

from pandas_schema import Column, Schema
from pandas_schema.validation import MatchesPatternValidation

from datamanagement.pii import commonregex
import json
import datetime


validation_funs = {
    "first_name": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "last_name": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "company_name": [MatchesPatternValidation(r'(?:\s*[a-zA-Z0-9,_\.\077\0100\*\+\&\#\'\~\;\-\!\@\;]{2,}\s*)*')],
    "address": [MatchesPatternValidation(r'\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St|Place)')],
    "city": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "county": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "state": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "province": [MatchesPatternValidation(r'^(?![ .]+$)[a-zA-Z .]*$')],
    "zip": [MatchesPatternValidation(commonregex.zip_code.pattern)],
    "postal": [MatchesPatternValidation(commonregex.zip_code.pattern)],
    "post": [MatchesPatternValidation(commonregex.zip_code.pattern)],
    "phone1": [MatchesPatternValidation(commonregex.phone.pattern)],
    "phone2": [MatchesPatternValidation(commonregex.phone.pattern)],
    "email": [MatchesPatternValidation(commonregex.email.pattern)],
    "web": [MatchesPatternValidation(commonregex.link.pattern)],
}

rules_definition = {
  "Must Be Populated": [MatchesPatternValidation(r'^(?!\s*$).+')], #r'/^$|\s+/'
  "Alphanumeric Only": [MatchesPatternValidation(r'^\w+$')],
  "Must be 7 digits": [MatchesPatternValidation(r'^\d{7}$')],
  "Numeric Only": [MatchesPatternValidation(r'^[0-9]*$')],
}

from pandas.core.common import flatten

ensure_list = lambda x: [x] if not isinstance(x, list) else x

def ruleTransformation(pyres):
  rules_dict = {}

  def ruleTransformations(cde: str, rule: set, regex: set):
    rules_val_fun = [rules_definition[x] for x in rule]  #map(lambda x: rules_definition[x], list(rule))
    regex_val_fun = [MatchesPatternValidation(r'{}'.format(regex))] if regex else [] #map(lambda x: MatchesPatternValidation(r'%s'.format(x)), [regex])
    total_rules = rules_val_fun + regex_val_fun
    return list(flatten(total_rules))


  for pyre in pyres:
    cde, rule_dict = pyre.item
    if isinstance(rule_dict, dict):  #type(rule_dict) is dict:
      rules_dict[cde] = ruleTransformations(cde, **rule_dict)

  return rules_dict

from pyrebase.pyrebase import Pyre
def ruleTransform(rule_pyres: List[Pyre], regex_pyres: List[Pyre]) -> Dict:
  rules_dict = {}
  regex_dict = dict([r.item for r in regex_pyres])

  def ruleTransformations(rule_set: set):
    rules_val_fun = [regex_dict[x] for x in rule_set]  #map(lambda x: rules_definition[x], list(rule))
    regex_val_fun = [MatchesPatternValidation(r'{}'.format(regex)) for regex in rules_val_fun] #map(lambda x: MatchesPatternValidation(r'%s'.format(x)), [regex])
    return regex_val_fun

  if rule_pyres:
    for pyre in rule_pyres:
      cde, rule_dict = pyre.item
      if isinstance(rule_dict, dict):  #type(rule_dict) is dict:
        rules_dict[cde] = ruleTransformations(rule_dict['rule'])

  return rules_dict




def myconverter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, datetime.datetime):
        return obj.__str__()

class DataErrors(DataDriver):

  def __init__(self, selected_dataset):
    super().__init__(selected_dataset)

  def val_funs(self, validation_funs):
    self.load_data(replace_empty_stings_with_NaNs = False)
    features = self.get_features_list()
    val_funs = {k:validation_funs[k] for k in validation_funs.keys() if k in features}
    return val_funs

  def create_columns(self, val_funs):
    columns = []
    for name, fun in val_funs.items():
        columns.append(Column(name, fun))
    return columns

  def create_schema(self, columns):
    try:
      return Schema(columns)
    except BaseException as error:
      raise error

  def errors(self, schema):
    _errors = schema.validate(self.data, columns=schema.get_column_names())
    # breakpoint()
    errors = [e.__dict__ for e in _errors if all(e.__dict__)]

    for err in errors:
      if not err['row'] == -1:
        primary_key = list(self.data)[0]
        err['Impacted_Key'] = primary_key
        err['Impacted_key_Value'] = self.data.iloc[err['row']][primary_key]

    return json.dumps(errors, default=myconverter)

  def save_errors(self, valid_funs):
    val_funs = self.val_funs(valid_funs)
    columns = self.create_columns(val_funs)
    # breakpoint()
    try:
      schema = self.create_schema(columns)
      errors = self.errors(schema)
      self.save_json(errors, paths.ERRORS_SUFFIX)
    except BaseException as error:
      print(f'Caught an error: {error}')
      print(f'It says "{error.args[0]}". Does it seem about right?')






def save_errors():
  datasets = pd.read_csv(paths.DATASETS)
  for index, dataset in datasets.iterrows():
    data_errors = DataErrors([*dataset, False])
    val_funs = data_errors.val_funs(validation_funs)
    columns = data_errors.create_columns(val_funs)
    schema = data_errors.create_schema(columns)
    errors = data_errors.errors(schema)
    data_errors.save_json(errors, paths.ERRORS_SUFFIX)
