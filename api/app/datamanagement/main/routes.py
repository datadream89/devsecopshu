import os
from pathlib import Path
import io
import csv
import requests

import jsonpickle
import pandas as pd
# import datacompy

import mysql.connector as MySQLdb

from flask import (render_template, send_file,
                    request, url_for, redirect,
                    session, Blueprint, flash)
from werkzeug.utils import secure_filename

from datamanagement.model.dataset import DataSet
from datamanagement.model.datasets import DataSets

from datamanagement.configuration import const_types

from datamanagement.configuration import paths

from datamanagement.main.utils import datasetuploaded, datatableuploaded #, puttables

from datamanagement.pii.utils import write_pii

from datamanagement.main.firebase import get_files

main = Blueprint('main', __name__)

# @main.before_app_first_request
def getmenu():
    #put tables in mysql
    # puttables()
    # breakpoint()
    # save_errors()
    if not os.path.isfile(paths.DATASETS_JSON):
        dataset_info = []

        # Read in CSV
        datasets_csv = pd.read_csv(paths.DATASETS)

        # Get title, filename, id, and label for each data set and add it to the collection
        for i, row in datasets_csv.iterrows():
            dataset_title = row["Title"]
            dataset_filename = row["FileName"]
            dataset_id = row["ID"]
            dataset_label = row["Label"]
            dataset = DataSet(dataset_filename, dataset_title, dataset_id, dataset_label)
            dataset_info.append(dataset)

        # Save the collection as JSON and return it
        datasets = DataSets(dataset_info=dataset_info)
        datasets_json = jsonpickle.encode(datasets)

        # Save the serialized JSON to a file
        with open(paths.DATASETS_JSON, 'w') as file:
            file.write(datasets_json)
    else:
        with open(paths.DATASETS_JSON, 'r') as serialized_file:
            json_str = serialized_file.read()
            datasets_json = jsonpickle.decode(json_str)

    get_files()

    return datasets_json

@main.route('/dataset_selection_changed', methods=['POST'])
def dataset_selection_changed():
    # Get the selected data set's name
    new_selection = str(request.form["data_set_field"])

    # Look up the Title, ID, Label (for existing data sets)
    datasets = pd.read_csv(paths.DATASETS)
    dataset = datasets.loc[datasets["FileName"] == new_selection]
    # breakpoint()
    if not dataset.empty: #if dataset is not None:
        new_title = dataset["Title"].values[0]
        new_index = dataset["ID"].values[0]
        new_label = dataset["Label"].values[0]

        # Save the selection in session
        session['data_file'] = new_selection
        session['data_title'] = new_title
        session['data_id'] = new_index
        session['data_label'] = new_label

    # Redirect and reload the appropriate page
    if request.referrer is not None:
        return redirect(request.referrer)
    else:
        return redirect(url_for('index'))

# @main.route('/dataComparision', methods=["GET", "POST"])
# def dataComparision():

#     if request.method == 'GET':
#         dataset_options = getmenu()
#         return render_template('dataComparision.html', dataset_options=dataset_options)
#     else:
#         data_selected_1 = str(request.form["data_set_field_1"])
#         data_selected_2 = str(request.form["data_set_field_2"])

#         # Look up the Title, ID, Label (for existing data sets)
#         datasets = pd.read_csv(paths.DATASETS)
#         dataset_1 = datasets.loc[datasets["FileName"] == data_selected_1]
#         dataset_2 = datasets.loc[datasets["FileName"] == data_selected_2]

#         session['dataset_comparision_1'] = dataset_1["Title"].values[0]
#         session['dataset_comparision_2'] = dataset_2["Title"].values[0]

#         from more_itertools import one
#         selected_dataset_1 = one(dataset_1.values.tolist()) + [False]
#         selected_dataset_2 = one(dataset_2.values.tolist()) + [False]

#         driver_1, driver_2 = DataDriver(selected_dataset_1), DataDriver(selected_dataset_2)
#         driver_1.load_data()
#         driver_2.load_data()

#         data_1 = driver_1.data
#         data_2= driver_2.data

#         compare = datacompy.Compare(data_1, data_2, on_index = True, df1_name='SOURCE', df2_name='DESTINATION')
#         report = compare.report()
#         idx = report.find('DataFrame Summary') #
#         dataset_options = getmenu()
#         return render_template('dataComparision.html', dataset_options=dataset_options, report=report[idx:])


@main.route('/getCompareReportCSV/<report>')
def compare_report_download(report):
    proxy = io.StringIO()

    writer = csv.writer(proxy)
    writer.writerow(str(report))

    # Creating the byteIO object from the StringIO Object
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    # seeking was necessary. Python 3.5.2, Flask 0.12.2
    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='compare_report.csv',
        mimetype='text/csv'
    )



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in const_types.ALLOWED_EXTENSIONS

def firebase_upload(selected_file: str):
  import pyrebase
  from datamanagement.configuration.key import FIREBASE_CONFIG
  from pathlib import Path

  firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
  storage = firebase.storage()
  files = storage.list_files()

  def get_filepath():
    for f in files:
      filename = f.name.split('/')[-1]
      filename = secure_filename(filename)
      if filename == selected_file:
        filepath = Path(paths.UPLOAD_FOLDER) / Path(filename).stem / filename
        if not filepath.exists():
          filepath.parent.mkdir(parents=True, exist_ok=True)
          f.download_to_filename(filepath)
        return filepath, filename
    else:
      print("The file is not found.")

  url = '/'.join(request.url.split('/')[:-1]) + '/upload_file'
  # filename = filename.name.split('/')[-1] #'downloaded_file.csv'
  # filename.download_to_filename(filename)
  filepath, filename = get_filepath()
  files = {'file': open(filepath, 'rb')}
  form = {'title': Path(filename).stem}
  requests.post(url, files=files, data=form)

  return filename


@main.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was passed into the request
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # Get the uploaded file
        file = request.files.get('file')
        glossary = request.files.get('glossary')
        validation = request.files.get('validation')

        # Check if a file was not selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If the file was uploaded and is an allowed type, proceed with upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # breakpoint()
            filepath = Path(paths.UPLOAD_FOLDER) / Path(filename).stem / filename
            if not filepath.exists():
              filepath.parent.mkdir(parents=True, exist_ok=True)
              file.save(filepath)

            glossary_filepath = Path(paths.UPLOAD_FOLDER) / Path(filename).stem / 'business_glossary.json'
            if glossary and not glossary_filepath.is_file():
                glossary.save(glossary_filepath)

            validation_filepath = Path(paths.UPLOAD_FOLDER) / Path(filename).stem / 'validation_rules.json'
            if validation and not validation_filepath.is_file():
                validation.save(validation_filepath)

            data_title = ""
            data_id = ""
            data_label = ""

            if "title" in request.form:
                data_title = request.form["title"]
            if "id" in request.form:
                data_id = request.form["id"]
            if "label" in request.form:
                data_label = request.form["label"]

            # breakpoint()

            # write_pii.delay(filename, pd.read_csv(filepath).to_json(), True)
            write_pii(filename, pd.read_csv(filepath).to_json(), True)

            # Move the file and set metadata
            datasetuploaded(uploaded_file_path=str(filepath),
                            data_title=data_title,
                            data_id=data_id,
                            data_label=data_label)

            # Return to the summary page and show the new data set info
            return redirect(url_for('controller.index'))
    else:
        dataset_options = getmenu()
        return render_template('upload.html', dataset_options=dataset_options)

def load_table(database,table):
	if 'login' not in session:
		return redirect(url_for("manageDB.ManageMyDB"))
	db = MySQLdb.connect(host=session['dbHost'],user=session['dbUsername'],passwd=session['dbPassword'])
	cursor = db.cursor()
	cursor.execute("Show databases")
	databases = cursor.fetchall()
	if not (database,) in databases:
		return redirect(url_for("manageDB.displayDatabases"))
	cursor.execute("use "+database)
	cursor.execute("show tables")
	tables = cursor.fetchall()
	if not (table,) in tables:
		return redirect(url_for("manageDB.displayDatabases")+"/"+database)
	cursor.execute("desc "+table);
	rows=cursor.fetchall()
	l=[]
	for row in rows:
		l.append(row[0])
	rows1=[]
	rows1.append(l)
	cursor.execute("select * from "+table);
	l=cursor.fetchall()
	rows1=rows1+list(l)
	cursor.close()
	db.close()
	return rows1


@main.route('/table_selection', methods=['GET', 'POST'])
def table_selection():
    if request.method == 'GET':
        # Check if a file was passed into the request
        if request.referrer:
            database_name, table_name = request.referrer.split('/')[-2:]
            session['database'] = database_name
            session['table'] = table_name

        filepath= os.path.join(paths.UPLOAD_FOLDER, table_name)

        table = load_table(database_name, table_name)
        headers = table.pop(0)
        df = pd.DataFrame(table, columns=headers)
        filename = os.path.join(filepath, table_name + '.csv')

        if not os.path.exists(filepath):
            os.makedirs(filepath)
            os.makedirs(os.path.join(filepath, "graphs"))

        with open(filename, "w") as f:
            df.to_csv(f, sep=',', index=False, encoding='utf-8')

        data_title = table_name
        data_id = ""
        data_label = ""

        if "label" in request.form:
            data_title = request.form["title"]
        if "id" in request.form:
            data_id = request.form["id"]
        if "label" in request.form:
            data_label = request.form["label"]
        # breakpoint()
        # Move the file and set metadata
        datatableuploaded(uploaded_file_path=str(filename),
                          data_title=data_title,
                          data_id=data_id,
                          data_label=data_label)

            # Return to the summary page and show the new data set info
        return redirect(url_for('controller.index'))
    else:
        dataset_options = getmenu()
        return render_template('database_upload.html', dataset_options=dataset_options)


@main.route('/database_upload', methods=['GET', 'POST'])
def database_upload():
    if request.method == 'POST':
        # Check if a file was passed into the request
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # Get the uploaded file
        file = request.files['file']

        # Check if a file was not selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If the file was uploaded and is an allowed type, proceed with upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(paths.UPLOAD_FOLDER, filename)
            file.save(filepath)

            data_title = ""
            data_id = ""
            data_label = ""

            if "label" in request.form:
                data_title = request.form["title"]
            if "id" in request.form:
                data_id = request.form["id"]
            if "label" in request.form:
                data_label = request.form["label"]

            # Move the file and set metadata
            datasetuploaded(uploaded_file_path=str(filepath),
                            data_title=data_title,
                            data_id=data_id,
                            data_label=data_label)

            # Return to the summary page and show the new data set info
            return redirect(url_for('index'))
    else:
        dataset_options = getmenu()
        if 'database' in session:
            return redirect(url_for('manageDB.displayDatabases', dataset_options=dataset_options))
        else:
            return render_template('database_upload.html', dataset_options=dataset_options)



@main.route('/experimental')
def experimental():
    return render_template('experimental.html')

