from pathlib import Path
from glob import glob
import json

from collections import defaultdict

from flask import (render_template, request,
                    jsonify, Blueprint, flash)

from datamanagement.controllers.data_driver import DataDriver
from datamanagement.controllers.data_summary import DataSummary
from datamanagement.controllers.data_univariate import DataUnivariate
# from datamanagement.controllers.data_bivariate import DataBivariate
from datamanagement.controllers.data_errors import DataErrors, validation_funs

from datamanagement.pii.PII_data_processor import (stem_restricted, word_match_stemming,
                                                    fuzzy_partial_stem_match)

from datamanagement.pii.utils import check_pii

from datamanagement.main.utils import getuploadeddataset, selecteddataset
from datamanagement.main.routes import getmenu

from datamanagement.configuration.paths import EXAMPLES_FOLDER, UPLOAD_FOLDER
from datamanagement.controllers.utils import (write_bussiness_terms,
                                               add_to_match_col, get_features,
                                               get_summary, get_errors)

# import tensorflow_data_validation as tfdv

# from tensorflow_data_validation import types
# from typing import Optional, Text
# from IPython.display import HTML

# from tensorflow_metadata.proto.v0 import anomalies_pb2
# from tensorflow_metadata.proto.v0 import schema_pb2
# from tensorflow_metadata.proto.v0 import statistics_pb2

controller = Blueprint('controller', __name__)

@controller.route('/')
@controller.route('/index')
def index():
    # data_file, data_title, data_id, data_label = selecteddataset()
    selected_dataset = selecteddataset()
    # dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()
    # breakpoint()
    driver = DataSummary(selected_dataset)
    # breakpoint()
    # Get the JSON for the summary data
    summary_json = driver.load_summary_json()
    error_msg = driver.get_error_msg()

    driver = DataUnivariate(selected_dataset)
    features_json = driver.load_features_json()

    pii_data = business_to_physical(selected_dataset, uploaded_dataset)

    return render_template('index.html',
                           summary_data=summary_json,
                           univariate_data=features_json,
                           data_file=selected_dataset[0],
                          #  dataset_options=dataset_options,
                           uploaded_dataset=uploaded_dataset,
                           pii_data=pii_data,
                           error_msg=error_msg)


@controller.route('/univariate')
def univariate():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()

    driver = DataUnivariate(selected_dataset)

    # Get the JSON for the summary data
    features_json = driver.load_features_json()
    error_msg = driver.get_error_msg()

    return render_template('univariate.html',
                           mydata=features_json,
                           data_file=selected_dataset[0],
                           dataset_options=dataset_options,
                           uploaded_dataset=uploaded_dataset,
                           error_msg=error_msg)


# @controller.route('/bivariate')
# def bivariate():
#     selected_dataset = selecteddataset()
#     dataset_options = getmenu()
#     uploaded_dataset = getuploadeddataset()

#     driver = DataBivariate(selected_dataset)

#     # Get the JSON for the summary data
#     interactions_json = driver.load_interactions_json()
#     error_msg = driver.get_error_msg()

#     return render_template('bivariate.html',
#                            data=interactions_json,
#                            data_file=selected_dataset[0],
#                            dataset_options=dataset_options,
#                            uploaded_dataset=uploaded_dataset,
#                            error_msg=error_msg)

def string_match(cols, look_up_word, threshold=0.75):
    identified_pii = []
    restricted_vars = look_up_word.split() #initialize_lists()
    restricted_vars, stemmer = stem_restricted(restricted_vars)

    identified_pii,_ = word_match_stemming(identified_pii, restricted_vars, cols, stemmer, False)
    identified_pii,_ = fuzzy_partial_stem_match(identified_pii, restricted_vars, cols, stemmer, threshold)
    # breakpoint()
    return identified_pii

# @controller.route('/autocomplete', methods=["GET"])
# def autocomplete():
#     pass

BUSINESS_GLOSSARY = ["First Name","Last Name","Company Name","Address","City","County","Province","State","Zip Code","Postal Code","Phone Number","Email","Website"]
col_names = ["first_name","last_name","company_name","address","city","county","state","zip","phone1","phone2","email","web"]
match = string_match(BUSINESS_GLOSSARY, col_names[0])



def business_to_physical(selected_dataset, uploaded_dataset):

    folder = UPLOAD_FOLDER if selected_dataset[-1] else EXAMPLES_FOLDER

    pii_file_path = Path(folder) / Path(selected_dataset[1]) / "pii_json.json"

    if not Path.exists(pii_file_path):
        driver = DataDriver(selected_dataset)
        driver.load_data()
        data = driver.data
        pii_data = check_pii(selected_dataset[0], data, uploaded_dataset[-1])
    # breakpoint()
    with open(pii_file_path) as fin:
        pairs = json.load(fin)

    pii_dict = {a:max(b, key=b.get) for a,b in pairs.items()}
    # pii_dict = {v: k for k, v in pii_dict.items()}

    return pii_dict

def load_json(json_file_path):
    with open(json_file_path) as fin:
        json_data = json.load(fin)
    return json_data

# @controller.route('/search', methods=['GET', 'POST'])
# def search():

#     selected_dataset = selecteddataset()
#     dataset_options = getmenu()
#     uploaded_dataset = getuploadeddataset()

#     driver = DataUnivariate(selected_dataset)

#     # Get the JSON for the summary data
#     features_json = driver.load_features_json()
#     # breakpoint()
#     error_msg = driver.get_error_msg()
#     if request.method == 'POST':
#         word = request.form['search']

#         cols = [i.feat_physical_name for i in features_json.features] #[i['feat_physical_name'] for i in features_json['features']]
#         match_cols = string_match(cols, word, threshold=0.95)

#         b_to_p = business_to_physical(selected_dataset)

#         if word in b_to_p:
#             match_cols.append(b_to_p[word])

#         try:
#             match_id = cols.index(match_cols[0])
#         except IndexError:
#             match_id = None

#         match = match_id != None
#         flash(f'Matched columns:{match_cols[0] if match_cols else None}', "info")
#         return render_template('search.html',
#                                 mydata=features_json,
#                                 data_file=selected_dataset[0],
#                                 dataset_options=dataset_options,
#                                 uploaded_dataset=uploaded_dataset,
#                                 error_msg=error_msg,
#                                 matched_term=match_cols,
#                                 match_id=match_id,
#                                 match=match)
#     else:
#         return render_template('search.html',
#                                 mydata=features_json,
#                                 data_file=selected_dataset[0],
#                                 dataset_options=dataset_options,
#                                 uploaded_dataset=uploaded_dataset,
#                                 error_msg=error_msg)

interested_feats = ['feat_physical_name', 'feat_vartype', 'feat_missing', 'feat_count', 'feat_outlierscore', 'feat_index', 'notes']

BUSINESS_GLOSSARY = ["First Name","Last Name","Company Name","Address","City","County","Province",
                     "State","Zip Code","Postal Code","Phone Number","Email","Website"]

def get_pii_dict(json_path):
    pii_json = load_json(json_path)
    pii_dict = {a:max(b, key=b.get) for a,b in pii_json.items()}
    return pii_dict

@controller.route('/search', methods=['GET', 'POST'])
def search():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()
    #get all the csv files only in subdirectories of datasets folder
    data_folders = glob(EXAMPLES_FOLDER + '/*/')

    if selected_dataset[-1]:
        data_folder = Path(UPLOAD_FOLDER) / selected_dataset[1]
        data_folders.append(data_folder)

    match_cols_total = {}
    summary_list = {}
    errors_list = {}

    if request.method == 'POST':
        word = request.form['search']
        for data_folder in data_folders:

            features_json = load_json(Path(data_folder) / 'features.json')
            cols = [i['feat_physical_name'] for i in features_json['features']]

            pii_dict= get_pii_dict(Path(data_folder) / 'pii_json.json')

            summary_json = load_json(Path(data_folder) / 'summary.json')
            errors_json = load_json(Path(data_folder) / 'errors.json')

            business_json = Path(data_folder) / 'business_terms.json'
            if business_json.is_file():
                business_terms = load_json(business_json)
            else:
                write_bussiness_terms(BUSINESS_GLOSSARY, cols, business_json)
                business_terms = load_json(business_json)


            #[i.feat_physical_name for i in features_json.features]
            match_cols = string_match(cols, word, threshold=0.95)

            dataset = Path(data_folder).name
            if match_cols:
                match_cols_total[dataset] = [get_features(i, interested_feats)
                                             for i in features_json['features']
                                              if i['feat_physical_name'] in match_cols] #match_cols #
                summary_list[dataset] = get_summary(summary_json, match_cols)
                errors_list[dataset] = get_errors(errors_json, match_cols)
            else:
                continue
            match_cols_total = add_to_match_col(match_cols_total, dataset, pii_dict, 'PII Type')
            match_cols_total = add_to_match_col(match_cols_total, dataset, business_terms, 'Business Name')
            b_to_p = {v: k for k, v in pii_dict.items()}

            # if word in b_to_p:
            #     match_cols_total[dataset].append(word)

        # [list(dict_val) for key,val in match_cols_total.items() for v in val for dict_val in v.values()]
        col_feat_values=[]
        for key,val in match_cols_total.items():
            for v in val:
                col_feat_values.append([key] + list(v.values()))
        # if col_feat_values:
        #     flash(f'Matched Tables:{list(match_cols_total.keys())}', "info")
        # else:
        #     flash(f'Found no match for the word.', "warning")
        if not col_feat_values:
            flash(f'Found no match for the word.', "warning")
        # breakpoint()
        features = ['Business_Name', 'feat_physical_name', 'PII_type', 'feat_vartype',
                     'feat_missing', 'feat_count', 'feat_outlierscore', 'feat_index', 'notes'] #rearrange the feature list to set an order of interest

        myorder = [0, -1, 1, -2, 3, 6, 4, 5, 2, -3]
        for lst in col_feat_values:
            lst = [lst[i] for i in myorder]
        col_feat_values = [[lst[i] for i in myorder] for lst in col_feat_values]


        return render_template("searchTerm.html",
                                data_file=selected_dataset[0],
                                dataset_options=dataset_options,
                                uploaded_dataset=uploaded_dataset,
                                features=features,
                                col_feat_values=col_feat_values,
                                columns=match_cols_total.keys(),
                                feature_values=match_cols_total.values(),
                                summary_list=summary_list,
                                errors_list=errors_list,
                                word=word)
    else:
        return render_template("searchTerm.html",
                                data_file=selected_dataset[0],
                                dataset_options=dataset_options,
                                uploaded_dataset=uploaded_dataset)



# def _add_quotes(input_str: types.FeatureName) -> types.FeatureName:
#   return "'" + input_str.replace("'", "\\'") + "'"


# def display_anomalies_html(anomalies: anomalies_pb2.Anomalies) -> Text:
#   """Displays the input anomalies.

#   Args:
#     anomalies: An Anomalies protocol buffer.
#   """
#   if not isinstance(anomalies, anomalies_pb2.Anomalies):
#     raise TypeError('anomalies is of type %s, should be an Anomalies proto.' %
#                     type(anomalies).__name__)

#   anomaly_rows = []
#   for feature_name, anomaly_info in anomalies.anomaly_info.items():
#     anomaly_rows.append([
#         _add_quotes(feature_name), anomaly_info.short_description,
#         anomaly_info.description
#     ])
#   if anomalies.HasField('dataset_anomaly_info'):
#     anomaly_rows.append([
#         '[dataset anomaly]', anomalies.dataset_anomaly_info.short_description,
#         anomalies.dataset_anomaly_info.description
#     ])

#   if not anomaly_rows:
#     return HTML('<h4 style="color:green;">No anomalies found.</h4>')
#   else:
#     # Construct a DataFrame consisting of the anomalies and display it.
#     anomalies_df = pd.DataFrame(
#         anomaly_rows,
#         columns=['Feature name', 'Anomaly short description',
#                  'Anomaly long description']).set_index('Feature name')
#     # Do not truncate columns.
#     pd.set_option('max_colwidth', -1)
#     return anomalies_df

@controller.route('/certify', methods=['GET', 'POST'])
def certify():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()

    folder = UPLOAD_FOLDER if selected_dataset[-1] else EXAMPLES_FOLDER

    pii_file_path = Path(folder) / Path(selected_dataset[1]) / "pii_json.json"
    import os
    filepath = Path(folder) / selected_dataset[1] / selected_dataset[0]
    # train_stats = tfdv.generate_statistics_from_csv(filepath)
    # schema = tfdv.infer_schema(statistics=train_stats)
    # anomalies = tfdv.validate_statistics(statistics=train_stats, schema=schema)
    # display_anomalies = display_anomalies_html(anomalies)

    return render_template('certify.html',
                                data_file=selected_dataset[0],
                                dataset_options=dataset_options,
                                uploaded_dataset=uploaded_dataset)
                                # post=display_anomalies

@controller.route('/searchAll', methods=['GET'])
def searchAll():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()
    #get all the csv files only in subdirectories of datasets folder
    data_folders = glob(EXAMPLES_FOLDER + '/*/')
    # features_json_list = Path(datasets).glob('*/features.json')
    # pii_json_list = Path(datasets).glob('*/pii_json.json')
    match_cols_total = {}
    summary_list = {}
    errors_list = {}

    for data_folder in data_folders:

        features_json = load_json(Path(data_folder) / 'features.json')
        cols = [i['feat_physical_name'] for i in features_json['features']]

        pii_json = load_json(Path(data_folder) / 'pii_json.json')
        pii_dict = {a:max(b, key=b.get) for a,b in pii_json.items()}
        summary_json = load_json(Path(data_folder) / 'summary.json')
        errors_json = load_json(Path(data_folder) / 'errors.json')

        business_json = Path(data_folder) / 'business_terms.json'
        if business_json.is_file():
            business_terms = load_json(business_json)
        else:
            write_bussiness_terms(BUSINESS_GLOSSARY, cols, business_json)
            business_terms = load_json(business_json)


        #[i.feat_physical_name for i in features_json.features]
        match_cols = cols #string_match(cols, word, threshold=0.95)

        dataset = Path(data_folder).name
        if match_cols:
            match_cols_total[dataset] = [get_features(i, interested_feats)
                                            for i in features_json['features']] #match_cols #
            summary_list[dataset] = get_summary(summary_json, match_cols)
            errors_list[dataset] = get_errors(errors_json, match_cols)
        else:
            continue
        match_cols_total = add_to_match_col(match_cols_total, dataset, pii_dict, 'PII Type')
        match_cols_total = add_to_match_col(match_cols_total, dataset, business_terms, 'Business Name')
        b_to_p = {v: k for k, v in pii_dict.items()}

        # if word in b_to_p:
        #     match_cols_total[dataset].append(word)

    # [list(dict_val) for key,val in match_cols_total.items() for v in val for dict_val in v.values()]
    col_feat_values=[]
    for key,val in match_cols_total.items():
        for v in val:
            col_feat_values.append([key] + list(v.values()))
    if col_feat_values:
        flash(f'Matched Tables:{list(match_cols_total.keys())}', "info")
    else:
        flash(f'Found no match for the word.', "warning")
    # breakpoint()
    return render_template("businessGlossary.html",
                            data_file=selected_dataset[0],
                            dataset_options=dataset_options,
                            uploaded_dataset=uploaded_dataset,
                            features=interested_feats + ['PII_type', 'Business_Name'],
                            col_feat_values=col_feat_values,
                            columns=match_cols_total.keys(),
                            feature_values=match_cols_total.values(),
                            summary_list=summary_list,
                            errors_list=errors_list)

@controller.route('/commentView', methods=['POST'])
def commentView():

    table_name = request.form['table']
    col_name = request.form['column']
    comment = request.form['comment']

    data_folder = Path(EXAMPLES_FOLDER) / table_name
    features_json = load_json(data_folder / 'features.json')

    #update the list of notes by adding the entered comment
    from more_itertools import one
    notes = one([feature['notes'] for feature in features_json['features'] if feature['feat_physical_name'] == col_name])
    notes.append(comment)

    #query the json data using objectpath
    import objectpath
    json_tree = objectpath.Tree(features_json)
    result = json_tree.execute(f"$.features[@.feat_physical_name is {col_name}].notes")

    #write to the file with the updated json
    with open(data_folder / 'features.json', 'w') as fin:
        json.dump(features_json, fin, indent=4)

    # breakpoint()

    if comment:
        table_col = table_name + col_name
        return jsonify({'table_column': table_col,
                        'comment': notes})

    return jsonify({'error': 'Missing data!'})

def validation_errors(selected_dataset, file):
    businessGlossary_data = load_json(file)
    matched = {k: string_match(validation_funs.keys(), v[0], threshold=0.75) for k, v in businessGlossary_data.items()}
    valid_funs = defaultdict(list)
    for k,v in matched.items():
        for i in v:
            valid_funs[k].extend(validation_funs[i])
    data_errors = DataErrors(selected_dataset)
    data_errors.save_errors(valid_funs)

def set_glossary(businessGlossary_data):
    glossary_terms = load_json('glossary.json')
    for k,v in businessGlossary_data.items():
        if not isinstance(v, list):
            businessGlossary_data[k] = [v, glossary_terms.get(v, None)]

@controller.route('/businessGlossary', methods=['GET'])
def businessGlossary():
    selected_dataset = selecteddataset()
    dataset_options = getmenu()
    uploaded_dataset = getuploadeddataset()

    folder = EXAMPLES_FOLDER if not selected_dataset[-1] else UPLOAD_FOLDER
    data_folder = Path(folder) / selected_dataset[1]
    file = Path(data_folder) / "business_glossary.json"

    businessGlossary_data = load_json(file)
    set_glossary(businessGlossary_data)
    businessGlossary_data = load_json('glossary.json')

    #validate the data and save the errors
    validation_errors(selected_dataset, file)

    return render_template("businessGlossary.html",
                            data_file=selected_dataset[0],
                            dataset_options=dataset_options,
                            uploaded_dataset=uploaded_dataset,
                            business_glossary=businessGlossary_data)





# import plotly
# import chart_studio.plotly as py
# import plotly.graph_objs as go
# import numpy as np
# import pandas as pd

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px

# df = [] #pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")

# def create_dashboard(server):
#     dash_app = dash.Dash(
#         server=server,
#         routes_pathname_prefix='/dashapp/'
#     )

#     dash_app.layout = html.Div([
#         html.Div([
#             html.Label(['NYC Calls for Animal Rescue']),
#             dcc.Dropdown(
#                 id='my_dropdown',
#                 options=[
#                         {'label': 'Action Taken by Ranger', 'value': 'Final Ranger Action'},
#                         {'label': 'Age', 'value': 'Age'},
#                         {'label': 'Animal Health', 'value': 'Animal Condition'},
#                         {'label': 'Borough', 'value': 'Borough'},
#                         {'label': 'Species', 'value': 'Animal Class'},
#                         {'label': 'Species Status', 'value': 'Species Status'}
#                 ],
#                 value='Animal Class',
#                 multi=False,
#                 clearable=False,
#                 style={"width": "50%"}
#             ),
#         ]),

#         html.Div([
#             dcc.Graph(id='the_graph')
#         ]),

#     ])

#     init_callbacks(dash_app)

#     return dash_app.server


# def init_callbacks(dash_app):
#     @dash_app.callback(
#         Output(component_id='the_graph', component_property='figure'),
#         [Input(component_id='my_dropdown', component_property='value')]
#     )

#     def update_graph(my_dropdown):
#         dff = df

#         piechart=px.pie(
#                 data_frame=dff,
#                 names=my_dropdown,
#                 hole=.3,
#                 )

#         return (piechart)


# @controller.route('/dashboard', methods=['GET'])
# def dashboard():
#     selected_dataset = selecteddataset()
#     dataset_options = getmenu()
#     uploaded_dataset = getuploadeddataset()
#     #get all the csv files only in subdirectories of datasets folder
#     data_folders = glob(EXAMPLES_FOLDER + '/*/')

#     if selected_dataset[-1]:
#         data_folder = Path(UPLOAD_FOLDER) / selected_dataset[1]
#         data_folders.append(data_folder)

#     errors_list = {}

#     for data_folder in data_folders:
#         dataset = Path(data_folder).name
#         errors_json = load_json(Path(data_folder) / 'errors.json')
#         errors_list[dataset] = Counter(err["column"] for err in errors_json)
#         # graphs.append()
#     errors_list_df = pd.DataFrame(errors_list)

#     graphs = []
#     for column in errors_list_df:

#         data = errors_list_df[column]
#         trace = go.Pie(
#             labels=data.index.values.tolist(),
#             values=data.tolist(),
#             name=list(data)[0]
#         )
#         data = [trace]
#         graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#         graphs.append(graphJSON)
#     if selected_dataset[-1]:
#         graph_1, graph_2, graph_3, graph_4, graph_5 = graphs
#     else:
#         graph_1, graph_2, graph_3, graph_4 = graphs
#         graph_5 = []
#     return render_template('dashboard.html',
#                             data_file=selected_dataset[0],
#                             dataset_options=dataset_options,
#                             uploaded_dataset=uploaded_dataset,
#                             errors_list=errors_list,
#                             graphs=graphs,graph_1=graph_1, graph_2=graph_2, graph_3=graph_3, graph_4=graph_4, graph_5=graph_5,
#                             columns=list(errors_list_df))





if __name__ == '__main__':
    app.run_server(debug=True)
