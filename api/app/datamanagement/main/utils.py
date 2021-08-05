import os

#import sqlalchemy
from pandas.io import sql


from flask import session

from datamanagement.configuration import paths

# import configparser
# config = configparser.ConfigParser()
# config.read('connection.ini')

# Server= config.get('SQL SERVER CONNECTION', 'Server')
# Database= config.get('SQL SERVER CONNECTION', 'Database')
# User= config.get('SQL SERVER CONNECTION', 'User')
# Password= config.get('SQL SERVER CONNECTION', 'Password')

def datasetuploaded(uploaded_file_path, data_title, data_id=None, data_label=None):
    # Create folder with graphs sub folder
    data_path = os.path.join(paths.UPLOAD_FOLDER, data_title)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        os.makedirs(os.path.join(data_path, "graphs"))

    # Move the uploaded file to this directory
    file_name = uploaded_file_path.split("/")[-1]
    # breakpoint()
    # os.rename(uploaded_file_path, str(data_path + "/" + file_name))

    # Update the list of options to select from
    session['data_file'] = file_name
    session['data_title'] = data_title
    session['data_id'] = data_id
    session['data_label'] = data_label

    # Set the uploaded one
    session['data_file_uploaded'] = file_name
    session['data_title_uploaded'] = data_title
    session['data_id_uploaded'] = data_id
    session['data_label_uploaded'] = data_label

def datatableuploaded(uploaded_file_path, data_title, data_id=None, data_label=None):
    # Create folder with graphs sub folder
    data_path = os.path.join(paths.UPLOAD_FOLDER, data_title)
    # breakpoint()
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if not os.path.exists(os.path.join(data_path, "graphs")):
        os.makedirs(os.path.join(data_path, "graphs"))

    # Move the uploaded file to this directory
    file_name = uploaded_file_path.split("/")[-1]
    # breakpoint()
    # if not db_table:
    #     os.rename(uploaded_file_path, str(data_path + "/" + file_name))

    # Update the list of options to select from
    session['data_file'] = file_name
    session['data_title'] = data_title
    session['data_id'] = data_id
    session['data_label'] = data_label

    # Set the uploaded one
    session['data_file_uploaded'] = file_name
    session['data_title_uploaded'] = data_title
    session['data_id_uploaded'] = data_id
    session['data_label_uploaded'] = data_label


def getuploadeddataset():
    data_file = None
    data_title = None
    data_id = None
    data_label = None

    if "data_file_uploaded" in session:
        data_file = session['data_file_uploaded']
    if "data_title_uploaded" in session:
        data_title = session['data_title_uploaded']
    if "data_id_uploaded" in session:
        data_id = session['data_id_uploaded']
    if "data_label_uploaded" in session:
        data_label = session['data_label_uploaded']
    # breakpoint()
    if data_file is not None and data_title is not None:
        return [data_file, data_title, data_id, data_label, True]

    return None

def session_file_exists(data_file):
    filepath = os.path.join(paths.EXAMPLES_FOLDER, data_file)
    filename = os.path.join(filepath, filepath + '.csv')
    return os.path.exists(filename)

def session_prune(data_file):
    if not session_file_exists(data_file):
        session.pop("data_file", None)
        session.pop("data_title", None)
        session.pop("data_id", None)
        session.pop("data_label", None)


def selecteddataset():
    data_file = None
    data_title = None
    data_id = None
    data_label = None
    data_uploaded = False

    #clear any outdated data file related variables in the session
    # session_prune(session["data_file"])

    # Check if the values are already in session
    if "data_file" in session:
        data_file = session['data_file']
    if "data_title" in session:
        data_title = session['data_title']
    if "data_id" in session:
        data_id = session['data_id']
    if "data_label" in session:
        data_label = session['data_label']
    if "data_file_uploaded" in session and session['data_file_uploaded'] == data_file:
        data_uploaded = True
    # breakpoint()
    # Make sure that at least the file and title are populated, or else get it from the page
    if data_file is None or data_title is None:
        # Get the current selected values
        data_file = "us-500.csv"
        data_title = "us-500"
        data_id = ""
        data_label = "first_name"
        data_uploaded = False

        # Save values in session for future requests
        session['data_file'] = data_file
        session['data_title'] = data_title
        session['data_id'] = data_id
        session['data_label'] = data_label

    return [data_file, data_title, data_id, data_label, data_uploaded]

def table_exists(db_con, tablename):
    dbcur=db_con.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

# def puttables():
#     # save_events(event)
#     datasets = paths.EXAMPLES_FOLDER
#     #get all the csv files only in subdirectories of datasets folder
#     csv_files = Path(datasets).glob('*/*.csv')
#     url = f'mysql+pymysql://{User}:{Password}@{Server}/{Database}' #https://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
#     # breakpoint()
#     engine = sqlalchemy.create_engine(url)
#     # con = engine.connect()
#     # try:
#     #     for csv_file in csv_files:
#     #         # if not table_exists(con, csv_file):
#     #         with open(csv_file, 'r') as f:
#     #             df_ = pd.read_csv(f, sep=',')
#     #         df_name = Path(csv_file).stem
#     #         df_.to_sql(con=con, name=df_name, if_exists='replace', index=False)
#     # # breakpoint()
#     # finally:
#     #     con.close()
#     try:
#         db_con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                                                format(User, Password, Server, Database))
#         # db_con = engine.connect()
#         for csv_file in csv_files:
#             with open(csv_file, 'r') as f:
#                 df_ = pd.read_csv(f, sep=',')
#             df_name = Path(csv_file).stem
#             df_.to_sql(con=db_con, name=df_name, if_exists='replace', index=False)
#         # breakpoint()
#     except Exception as e:
#         print(e)
