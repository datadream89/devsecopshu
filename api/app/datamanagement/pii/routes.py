import heapq
import json
import os
from collections import defaultdict

import pandas as pd

from pathlib import Path

from flask import Flask, render_template, request, jsonify, url_for, redirect, session, Blueprint

from datamanagement.main.utils import getuploadeddataset, selecteddataset
from datamanagement.main.routes import getmenu

from datamanagement.controllers.data_summary import DataSummary
from datamanagement.controllers.data_driver import DataDriver

from datamanagement.pii.utils import check_pii


from datamanagement.configuration.paths import EXAMPLES_FOLDER, UPLOAD_FOLDER

pii = Blueprint('pii', __name__)



@pii.route('/discoverPii')
def discoverPii():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()
    # breakpoint()
    driver = DataDriver(selected_dataset)
    driver.load_data()
    data = driver.data
    error_msg = driver.get_error_msg()
    # breakpoint()
    pii_data = check_pii(selected_dataset[0], data.to_json(), selected_dataset[-1])
    # breakpoint()
    pii_entities = pii_data.index.values
    pii_rows = map(list, pii_data.values)
    pii_cols = list(pii_data)
    driver = DataSummary(selected_dataset)

    # Get the JSON for the summary data
    summary_json = driver.load_summary_json()
    error_msg = driver.get_error_msg()
    return render_template('showPii.html',
                           data_file=selected_dataset[0],
                           dataset_options=dataset_options,
                           uploaded_dataset=uploaded_dataset,
                           error_msg=error_msg,
                           pii_rows=pii_rows,
                           pii_cols=pii_cols,
                           rownames=pii_entities,
                           IDs=zip(pii_entities, pii_rows))



def pii_anomalies(selected_dataset):

    # script_dir = os.path.dirname(__file__)
    # rel_path = "pii_json.json"
    # abs_file_path = os.path.join(script_dir, rel_path)
    folder = UPLOAD_FOLDER if selected_dataset[-1] else EXAMPLES_FOLDER

    pii_file_path = Path(folder) / Path(selected_dataset[1]) / "pii_json.json"

    # abs_file_path = Path(EXAMPLES_FOLDER) / Path(selected_dataset[1]) / "pii_json.json"

    if not os.path.exists(pii_file_path):
        driver = DataDriver(selected_dataset)
        driver.load_data()
        data = driver.data
        pii_data = check_pii(selected_dataset[0], data, selected_dataset[-1])

    with open(pii_file_path) as fin:
        pairs = json.load(fin)

    n=2
    TwoHighest = {a:heapq.nlargest(n, b, key = b.get) for a,b in pairs.items()}
    def_dict = defaultdict(dict)
    for key, vals in TwoHighest.items():
        for val in vals:
            def_dict[key][val] = pairs[key][val]

    return def_dict


@pii.route('/certify')
def certify():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()

    pii_dict = pii_anomalies(selected_dataset)
    return render_template('certify.html',
                           data_file=selected_dataset[0],
                           dataset_options=dataset_options,
                           uploaded_dataset=uploaded_dataset,
                           pii_dict=pii_dict)


