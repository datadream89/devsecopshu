"""
This script runs the FlaskWebProject2 application using a development server.
"""


import os
from typing import List
import json


from pathlib import Path

from datamanagement.configuration import paths
from datamanagement.main.routes import firebase_upload

from flask import (render_template,
                    request, jsonify, send_file,
                    session, Blueprint)

angular_routes = Blueprint('angular_routes', __name__)

@angular_routes.before_request
def intialize_variables():
  session['existing_rules_list'] = dict()
  session['existing_rules_list_status_done'] = False
  print("before_request is running!")

@angular_routes.after_request
def undo_variable_setting(response):
  session['existing_rules_list_status_done'] = True
  return response

import pickle
angular_route_path = os.path.abspath(os.path.dirname(__file__))
data_list = []
def session_load():
  session_new = {}
  try:
    with open(f'{angular_route_path}/session_saved.pkl', 'rb') as input:
      session_saved = pickle.load(input)
  except Exception as e:
    print(f'threw exception of {e}')
    return None, None
  for k,v in session_saved.items():
    session_new[k] = v

  data_list = list(map(session_new.get, ['data_file', 'data_title', 'data_id', 'data_label', 'data_uploaded']))
  return session_new, data_list

session_new, selected_dataset = session_load()

@angular_routes.route("/profiling")
def profiling():
  session_new, _ = session_load()
  filename = session_new['data_file'] #firebase_upload(session["data_file"])
  filepath = Path(paths.UPLOAD_FOLDER) / Path(filename).stem / 'features.json'
  with open(str(filepath), 'r') as data_file:
    json_data = json.load(data_file)
  json_data['data'] = json_data.pop('features')
  #replace `None` with ''
  r = json.dumps(json_data).replace('null', '')
  json_data = json.loads(r)
  return jsonify([json_data])


from datamanagement.controllers.data_summary import DataSummary
from datamanagement.controllers.data_univariate import DataUnivariate
from datamanagement.controllers.pandas_profiling import PandasProfiling


@angular_routes.route("/pandas_profiling")
def pandas_profiling():
  _, selected_dataset = session_load()

  driver = PandasProfiling(selected_dataset)
  profiling_html = driver.get_profiling_html()
  return send_file(profiling_html)  #render_template(profiling_html)

@angular_routes.route("/expectations_rules")
def expectations_rules():
  _, selected_dataset = session_load()

  driver = PandasProfiling(selected_dataset)
  profile = driver.get_profiling_html(as_html=True)
  suite, data_context = driver.get_expectation_suite(profile)
  driver.run_validation(suite, data_context)
  return "OK", 200

@angular_routes.route("/summary_stats")
def summary_stats():
  _, selected_dataset = session_load()

  driver = DataSummary(selected_dataset)

  summary_json = driver.load_summary_json()
  return jsonify(summary_json.__dict__)

@angular_routes.route("/frequency_stats")
def frequency_stats():
  _, selected_dataset = session_load()

  driver = DataUnivariate(selected_dataset)

  frequency_json = driver.load_frequency_json()
  return jsonify(frequency_json)


@angular_routes.route("/files")
def files_history():
  """API for the file names in the uploads folder under static directory

  Returns:
      json_data: json with the key `files` and the value list of dir names
  """
  p = Path(paths.UPLOAD_FOLDER)
  subdir = [x.stem for x in p.iterdir() if x.is_dir()]
  json_data={'files':subdir}
  return jsonify(json_data)

from datamanagement.controllers.data_errors import DataErrors, ruleTransform
from datamanagement.controllers.data_rules import Rules, dbHandler, RULES_TABLE, REGEX_TABLE

db = dbHandler()
@angular_routes.route("/certification", methods=["GET", "POST"])
def certification():

  pyres = db._dbHandle.child('rules').get().pyres
  _, selected_dataset = session_load()
  data_errors = DataErrors(selected_dataset)
  validation_funcs = ruleTransform(pyres)
  data_errors.save_errors(validation_funcs)
  errors_json = data_errors.load_json(paths.ERRORS_SUFFIX)
  exceptions = {"data": errors_json}
  return jsonify([exceptions])

from datamanagement.controllers.data_pii import DataPii
@angular_routes.get("/pii_classification")
def pii_classification():
  _, selected_dataset = session_load()
  driver = DataPii(selected_dataset)

  pii_flare_json = driver.load_pii_flare_json()
  return jsonify(pii_flare_json)


@angular_routes.post("/apply_rules")
def apply_rules():
  cde = request.form.get('cde')

  import ast
  rule: List[str] = ast.literal_eval(request.form.get('rulename'))

  regex_pattern: List[str] =request.form.get('regex_pattern')
  regex_description = request.form.get('regex_description')

  #commit the regex and description to the table
  if regex_description and regex_pattern:
    db.add_rules(tableName=REGEX_TABLE, keyName=regex_description, data=regex_pattern)

  #profiling methods use location data and persist on mongodb or any database
  if regex_description:
    rule.append(regex_description)
  data = {'rule': rule}

  db.add_rules(tableName=RULES_TABLE, keyName=cde, data=Rules(**data))
  return jsonify(data)

@angular_routes.post("/delete_rules")
def delete_rules():
  cde = request.form.get('cde')

  import ast
  rule: List[str] = ast.literal_eval(request.form.get('rulename'))

  #profiling methods use location data and persist on mongodb or any database
  data = {'rule': rule}

  db.remove_rules(tableName=RULES_TABLE, keyName=cde, data=Rules(**data))
  return jsonify(data)



@angular_routes.get('/dropdown_rules')
def dropdown_rules():
  return jsonify({"key": [pyre.key() for pyre in db.get_table_childs(REGEX_TABLE)]})


@angular_routes.post('/existing_rules')
def get_existing_rules():
  cde_name = request.form.get('cde')
  return jsonify({"key": db.get_record(RULES_TABLE, cde_name).get('rule', [])})


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output)

import os
os.environ["PYTHONHTTPSVERIFY"] = "0"

from datamanagement.main.utils import datasetuploaded
from werkzeug.utils import secure_filename
@angular_routes.route("/postfiles", methods=['GET','POST'])
def postfiles():

  filename_in_bytes = request.data
  filename =  filename_in_bytes.decode()
  filename = secure_filename(filename)
  filetitle = Path(filename).stem

  datasetuploaded(filename, filetitle)
  # Update the list of options to select from
  session['data_file'] = filename
  session['data_title'] = filetitle

  # Set the uploaded one
  session['data_file_uploaded'] = filename
  session['data_title_uploaded'] = filetitle
  session['data_uploaded'] = True

  save_object(dict(session), f'{angular_route_path}/session_saved.pkl')

  firebase_upload(filename)

  return filename


@angular_routes.route('/exceptions', methods=['GET', 'POST'])
def exceptions():
  db = dbHandler()
  rule_pyres = db._dbHandle.child('rules').get().pyres
  regex_pyres = db._dbHandle.child('regexes').get().pyres
  _, selected_dataset = session_load()
  data_errors = DataErrors(selected_dataset)
  validation_funcs = ruleTransform(rule_pyres, regex_pyres)
  data_errors.save_errors(validation_funcs)
  returned_json =  data_errors.load_json(paths.ERRORS_SUFFIX) or \
   [{
    "Impacted_Key": "----",
    "Impacted_key_Value": "----",
    "column": "----",
    "message": "----",
    "row": "----",
    "value": "----"
  }]

  returned_json = {"data": returned_json}
  return jsonify([returned_json])


@angular_routes.route('/advanced_profiling')
def advanced_profiling():

    location = request.form.get('name')
    user = request.form.get('user')
    password = request.form.get('password')
    dbname = request.form.get('dbname')
    schema = request.form.get('schema')
    table = request.form.get('table')

    print(location)
    #profiling methods use location data and persist on mongodb or any database
    result = {'data': {'id':1, 'name':location,'user':user,'dbname':dbname,'schema':schema,'table':table}}
    print(result)
    return render_template('./profiling.html')



@angular_routes.route('/unstructured')
def unstructured():

    return '''<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem"><div class="entities" style="line-height: 2.5; direction: ltr">Subject line: Overdue invoice SD123567456 for  <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     Dell     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">ORG</span> </mark>  computer due  <mark class="entity" style="background: #bfe1d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     4/17/2021     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">DATE</span> </mark>  </br>  <mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     Hi Brian     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PERSON</span> </mark> , </br> I hope you’re well! We’re yet to receive payment for invoice number SD123567456 for Windows10 laptop, purchased on  <mark class="entity" style="background: #ffeb80; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     Black Friday     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">EVENT</span> </mark>  2020 which was due on  <mark class="entity" style="background: #bfe1d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     4/17/2021     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">DATE</span> </mark> . Please let us know when we can expect to receive payment of $ <mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     2050     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">MONEY</span> </mark> , and don’t hesitate to reach out if you have any questions or concerns. </br> Kind regards, </br>  <mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">     Micheal Davis     <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PERSON</span> </mark> </div></div>'''

@angular_routes.route('/unstructured_text')
def unstructured_text():

    return '''Subject line: Overdue invoice SD123567456 for Dell computer due 4/17/2021 <br>
 Hi Brian, <br>
 I hope you’re well! We’re yet to receive payment for invoice number SD123567456 for Windows10 laptop, purchased on Black Friday 2020 which was due on 4/17/2021. Please let us know when we can expect to receive payment of $2050, and don’t hesitate to reach out if you have any questions or concerns. <br>
 Kind regards, <br>
 Micheal Davis'''



# from typing import Dict
# from pyspark.sql import SparkSession, Row
# import pydeequ


# # Installed python3.6 for this section https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/

# import os
# os.environ['PYSPARK_PYTHON']="/home/bharath/Downloads/FastApi-tutorials/env36/bin/python"
# os.environ['PYSPARK_DRIVER_PYTHON']="/home/bharath/Downloads/FastApi-tutorials/env36/bin/python"
# os.environ['PYSPARK_DRIVER_PYTHON']="/home/bharath/Downloads/FastApi-tutorials/env36/lib/python3.6/site-packages/pyspark"

# # spark = SparkSession.builder.master("local").getOrCreate()
# # spark.sparkContext.addPyFile("/home/bharath/Downloads/deequ-1.0.3.jar")

# spark = (SparkSession
#     .builder
#     .config("spark.jars.packages", pydeequ.deequ_maven_coord)
#     .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
#     .getOrCreate())

# df = spark.sparkContext.parallelize([
#             Row(a="foo", b=1, c=5),
#             Row(a="bar", b=2, c=6),
#             Row(a="baz", b=3, c=None)]).toDF()


# @angular_routes.get('/ruleSuggestions')
# def ruleSuggestions(): #current_user:schemas.User = Depends(oauth2.get_current_user)
#   """
#   Generate suggestions for the rules to be applied on the column profiles computed from
#   the data.
#   """
#   from pydeequ.suggestions import ConstraintSuggestionRunner, DEFAULT

#   suggestionResult = ConstraintSuggestionRunner(spark) \
#              .onData(df) \
#              .addConstraintRule(DEFAULT()) \
#              .run()
#   print(suggestionResult)
#   return 'OK', 200

# @angular_routes.put('/applyRules')
# def applyRules(): #, current_user:schemas.User = Depends(oauth2.get_current_user)
  # """
  # Apply the rule checks and required analysis and get the results returned.
  # Results include all the metrics generated during the run.
  # """
  # from pydeequ.checks import Check, CheckLevel
  # from pydeequ.verification import VerificationSuite,VerificationResult

  # check = Check(spark, CheckLevel.Warning, "Review Check")

  # checkResult = VerificationSuite(spark) \
  #     .onData(df) \
  #     .addCheck(
  #         check.hasSize(lambda x: x >= 3) \
  #         .hasMin("b", lambda x: x == 0) \
  #         .isComplete("c")  \
  #         .isUnique("a")  \
  #         .isContainedIn("a", ["foo", "bar", "baz"]) \
  #         .isNonNegative("b")) \
  #     .run()

  # checkResult_df = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
  # return checkResult_df.show()



