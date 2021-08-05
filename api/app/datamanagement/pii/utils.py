#https://www.dataquest.io/blog/pandas-big-data/

import os
import warnings
from pathlib import Path
# from pii_analyzer import PiiAnalyzer

from datamanagement.configuration.paths import EXAMPLES_FOLDER, UPLOAD_FOLDER

from datamanagement.pii.analyzer import AnalyzerEngine
from datamanagement.pii.analyzer.logger import Logger

from datamanagement.pii.commonregex import CommonRegex, regexes
# from datamanagement import celery

import usaddress
import spacy
nlp = spacy.load('en_core_web_sm')

import collections
from collections import Counter
from collections import defaultdict

# import streamlit as st
import pandas as pd
# import datacompy
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
# import tkinter as tk
# from tkinter import filedialog
from datetime import datetime

# from IPython.display import IFrame
from pandas_profiling import ProfileReport
# from pandas_summary import DataFrameSummary

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

BUCKET_NAME = "rewrite-streaming-dev-bharath2"
ACCESS_KEY = 'AKIAJW2WGLIC7QHGE7DA'
SECRET_KEY = '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'
REGION_NAME = 'us-west-2'

logger = Logger()

def makehash():
    return collections.defaultdict(makehash)

class PiiAnalyzer(object):
    def __init__(self, df):
        self.df = df
        self.parser = CommonRegex()
        self.nlp_model = spacy.load('en')
        # self.standford_ner =  StanfordNERTagger('classifiers/english.conll.4class.distsim.crf.ser.gz') #spacy.load("spacy/spacyNER")


    def analysis(self):
        people = []
        organizations = []
        locations = []
        emails = []
        phone_numbers = []
        phones_with_exts = []
        street_addresses = []
        btc_addresses = []
        credit_cards = []
        ips = []
        dates = []
        zip_codes = []
        po_boxes = []
        ssn_number = []
        data = []

        dic = {}
        dic2 = defaultdict(list)

        # with open(self.filepath, 'rU') as filedata:
        #     reader = csv.reader(filedata)
        logger.info(f'the data argument passed to PiiAnalyzer is of the type: {type(self.df)}')

        for j, row in self.df.iterrows():
            data.extend(row)
            for i, text in enumerate(row):
                text = str(text)
                if self.parser.emails(text):
                    emails.extend(self.parser.emails(text))
                    dic2[i].append('email')
                if self.parser.phones("".join(text.split())):
                    phone_numbers.extend(self.parser.phones("".join(text.split())))
                    dic2[i].append('phone_number')
                if self.parser.street_addresses(text):
                    street_addresses.extend(self.parser.street_addresses(text))
                    dic2[i].append('street_address')
                if self.parser.credit_cards(text):
                    credit_cards.extend(self.parser.credit_cards(text))
                    dic2[i].append('credit_cards')
                if self.parser.ips(text):
                    ips.extend(self.parser.ips(text))
                    dic2[i].append('ip')
                if self.parser.dates(text):
                    dates.extend(self.parser.ips(text))
                    dic2[i].append('dates')
                if self.parser.zip_codes(text):
                    zip_codes.extend(self.parser.ips(text))
                    dic2[i].append('zip_codes')
                if self.parser.po_boxes(text):
                    po_boxes.extend(self.parser.ips(text))
                    dic2[i].append('po_boxes')
                if self.parser.ssn_number(text):
                    ssn_number.extend(self.parser.ips(text))
                    dic2[i].append('ssn_number')
                if self.parser.phones_with_exts(text):
                    phones_with_exts.extend(self.parser.ips(text))
                    dic2[i].append('phones_with_exts')
                if self.parser.btc_addresses(text):
                    btc_addresses.extend(self.parser.ips(text))
                    dic2[i].append('btc_addresses')

                parsed_doc = nlp(text)
                for ent in parsed_doc.ents:
                    if ent.label_ == 'PERSON':
                        people.append(ent.text)
                        dic2[i].append('person')
                    if ent.label_ == 'GPE':
                        locations.append(ent.text)
                        dic2[i].append('location')
                    if ent.label_ == 'ORG':
                        organizations.append(ent.text)
                        dic2[i].append('organization')

            dic[j] = {'people': people, 'locations': locations, 'organizations': organizations,
                      'emails': emails, 'phone_numbers': phone_numbers, 'street_addresses': street_addresses,
                      'credit_cards': credit_cards, 'ips': ips,
                      }

        # for title, tag in self.standford_ner.tag(set(data)):
        #     if tag == 'PERSON':
        #         people.append(title)
        #     if tag == 'LOCATION':
        #         locations.append(title)
        #     if tag == 'ORGANIZATION':
        #         organizations.append(title)

        # for parsed_doc in self.nlp_model.pipe(str(data), batch_size=1, n_threads=4):
        #     print(parsed_doc)
        #     for ent in parsed_doc.ents:
        #         if ent.label_ == 'PERSON':
        #             people.append(ent.text)
        #         if ent.label_ == 'LOCATION':
        #             locations.append(ent.text)
        #         if ent.label_ == 'ORG':
        #             organizations.append(ent.text)

        def column_wise_analysis(self):
            # dic = ['people' : [],
            # 'organizations' : [],
            # 'locations' : []]
            dic = makehash()
            for (colName, colData) in self.data.iteritems():
                for key in regexes.keys():
                    if not key in ['street_addresses']:
                        dic[colName][key] = colData.apply(lambda x: next(iter(getattr(self.parser, key)(x)))).count()
                    else:
                        dic[colName][key] = colData.apply(lambda x: len(set([t[1] for t in usaddress.parse(x)])) >= 3).count()

            st.json(json.dumps(dic))
            return dic






        return dic, dic2

# def memory_usage(df):
#     return round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2)
#
# with open('column_types_1.json', 'r') as f:
#     column_types_1 = json.load(f)

# df = pd.read_csv('pii_data.csv', index_col=0)
#



def text_analyzer(my_text, all_fields=True, score_threshold=0.5):
    engine = AnalyzerEngine(enable_trace_pii=True)
    response = engine.analyze(correlation_id=0,
                              text=my_text,
                              entities=[],
                              language='en',
                              all_fields=all_fields,
                              score_threshold=score_threshold)
    # allData = ["start = {}, end = {}, entity = {}, confidence = {}". format(item.start,
    #                                                                    item.end,
    #                                                                    item.entity_type,
    #                                                                    item.score) for item in response]
    allData = [{'start': item.start, 'end': item.end, 'entity': item.entity_type,
                'confidence': item.score} for item in response]

    return allData

# print(text_analyzer("\t".join(str(df['PHHO']).strip())))
# print(text_analyzer(str(df['PHHO'].values).strip()))
# print('.')
# print(text_analyzer(str(df['PHHO'])))

class myCommonRegex(CommonRegex):

    def __init__(self, ind, text=""):
        super().__init__(text)
        self.ind = ind

# # print("\t".join(str(df['PHHO']).strip()))
#
# # for key, value in df.iteritems():
# #     parsed_text = myCommonRegex(key, str(value).strip())
# #     attributes = inspect.getmembers(parsed_text, lambda a: not (inspect.isroutine(a)))
# #     pii = set(
# #         {k: v for k, v in dict([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]).items()
# #          if v}.keys()) - set(['ind', 'text'])
# #     if pii:
# #         print({parsed_text.ind: pii})

#
# print(dct)
# # parsed_text = myCommonRegex(1, str(df['PHHO'].values).strip())
# # attributes = inspect.getmembers(parsed_text, lambda a:not(inspect.isroutine(a)))
# # [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
# # pii = set({k: v  for k, v in dict([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]).items() if v}.keys()) - set(['ind', 'text'])
# # return {myCommonRegex.ind: pii}
#
# # for parsed_doc in nlp.pipe(iter(df['A3S4']), batch_size=1, n_threads=4):
# #     for ent in parsed_doc.ents:
# #         print(ent.text, ent.label_)
#
# # for parsed_doc in nlp.pipe(iter(df['A2S4']), batch_size=1, n_threads=4):
# #     for ent in parsed_doc.ents:
# #         print(ent.text, ent.label_)

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME)
    logger.info("Uploading to AWS")
    try:
        s3.put_object(Body=local_file, Bucket=bucket, Key=s3_file)
        logger.debug('Upload Successful')
        return True
    except FileNotFoundError:
        logger.exception("The file was not found")
        return False
    except NoCredentialsError:
        logger.exception("Credentials not available")
        return False

# @st.cache
def create_bucket(bucket_name='data-profiling'):
    logger.info(f"Checking for the bucket: {bucket_name}")
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME)
    response = s3.list_buckets()
    logger.info(f'Existing buckets: {response}')

    if not any(bucket['Name'] == bucket_name for bucket in response['Buckets']):
        # bucket_name = 'data-profiling'
        logger.info(f"Bucket {bucket_name} not found so creating one")
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': REGION_NAME})

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': "arn:aws:s3:::%s/*" % bucket_name
            }]
        }
        bucket_policy = json.dumps(bucket_policy)

        try:
            s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        except ClientError as err:
            logger.error(f"{bucket_name} does not seem to exist under the policy {bucket_policy}")
        except Exception as e:
            logger.error(e)

        try:
            s3.put_bucket_website(
                Bucket=bucket_name,
                WebsiteConfiguration={
                    'ErrorDocument': {'Key': 'error.html'},
                    'IndexDocument': {'Suffix': 'index.html'},
                }
            )
        except ClientError as e:
            logger.error(e)
    logger.debug("Website is hosted in AWS")

# @st.cache
def put_website(bucket_name, index_file, error_file):
    logger.info(f"putting website in the bucket {bucket_name}")
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME)

    filename = [index_file, error_file]

    for file in filename:
        data = open(file, 'rb') #encoding='utf-8'
        try:
            s3.put_object(Body=data,
                          Bucket=bucket_name,
                          Key=file,
                          ContentType='text/html')
        except Exception as e:
            logger.error(e)
        else:
            data.close()
            logger.info("Bucket loaded with object")
        finally:
            logger.info("exiting putting website")

# @st.cache
def bucket_last_modified(bucket_name: str) -> datetime:
    """
    Given an S3 bucket, returns the last time that any of its objects was
    modified, as a timezone-aware datetime.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    objects = list(bucket.objects.all())
    return max(obj.last_modified for obj in objects)

text = 'My name is David and I live in Miami and my email id baan@email.com my credit card is 4938385567019561 my number is 573 7840970 and i work at Microsoft in Seattle'


# @st.cache
def text_analyzer(my_text, all_fields=True, score_threshold=0.5):
    engine = AnalyzerEngine(enable_trace_pii=True)
    response = engine.analyze(correlation_id=0,
                              text=my_text,
                              entities=[],
                              language='en',
                              all_fields=all_fields,
                              score_threshold=score_threshold)
    # allData = ["start = {}, end = {}, entity = {}, confidence = {}". format(item.start,
    #                                                                    item.end,
    #                                                                    item.entity_type,
    #                                                                    item.score) for item in response]
    allData = [{'start': item.start, 'end': item.end, 'entity': item.entity_type,
                'confidence': item.score} for item in response]
    return allData

def mask(text, pii):

    for p in pii:
        text = text[:p['start']] + '<' + p['entity'] + '>' + text[p['end']:]
    return text

def mergeDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]

    return dict3


# @st.cache
def get_pii_columns(df):
    logger.info(f'the data argument passed to get_pii_columns is of the type: {type(df)}')
    logger.info(df.head(2))
    # logger.info(df.apply(str).head(2))
    # piianalyzer = PiiAnalyzer(df.apply(str))
    piianalyzer = PiiAnalyzer(df)
    # logger.info()
    analysis1, analysis2 = piianalyzer.analysis()

    analysis3 = dict()
    for k, v in analysis2.items():
        analysis3[df.columns[k]] = Counter(v)

# with open("analysis1.json", "w") as f:
#     f.write(json.dumps(analysis1))
#
# with open("analysis2.json", "w") as f:
#     f.write(json.dumps(analysis2))

# print(analysis)
    logger.info('generating the second dict')
    dct = {}
    for key, value in df.iteritems():
        lst = []
        for parsed_text in nlp.pipe(iter(value), batch_size=1, n_threads=4): #nlp.pipe(iter(value.apply(str)), batch_size=1, n_threads=4):
            for ent in parsed_text.ents:
                if not ent.label_ == 'CARDINAL' and not ent.label_ == 'DATE':
                    lst.append(ent.label_)
        dct[key] = Counter(lst)

    d = mergeDict(analysis3, dct)
    d1 = {k: sum(v, Counter()) for k, v in d.items()}
    d2 = {k: max(v.items(), key=lambda x: x[1]) for k, v in d1.items() if v}

    df1 = pd.DataFrame(d2.items(), columns=['Pii_Column', 'Pii_Classification'])
    df1['Anamoly_Score'] = df1['Pii_Classification'].apply(lambda x: (df.shape[0] - x[1]) / df.shape[0])

    return df1


# @st.cache
# def profiling(data, website_bucket_name, profile_file):
#     logger.info('generating pandas profiling')
#     profile = ProfileReport(data,
#                             minimal=True)  # , title='Pandas Profiling Report', html={'style': {'full_width': True}}) #, check_correlation=False)
#     # profile_file = "index.html"
#     logger.info('saving the pandas profiling report')
#     profile.to_file(output_file=profile_file)
#     IFrame(src="./index.html", width=700, height=600)

#     logger.info('create a bucket for hosting the profiling report')

#     create_bucket(website_bucket_name)
#     put_website(website_bucket_name, index_file="index.html", error_file='error.html')

#     return profile_file

# def classfication(data):
#     st.title('PII Classification')
#     st.subheader('Discover PII in the data')
#     # response1 = text_analyzer(data)

#     Key = "lambda//"
#     outPutname = "PII_Structered"
#     # st.subheader('Process the data to discover the PII and classification')
#     if st.button('Process File'):
#         # st.json(json.dumps(get_pii_columns(data.iloc[:, 30:40])))
#         # st.dataframe(data)
#         st.dataframe(get_pii_columns(data)) #data.iloc[:, 30:40]

# def check_streetaddress(data):
#     if st.button('check streetaddress'):
#         parser = CommonRegex()

#         st.dataframe(data)

#         st.dataframe(data.apply(lambda x: next(iter(parser.street_addresses(x)), '')))

#         st.dataframe(data.apply(lambda x: len(set([t[1] for t in usaddress.parse(x)]))) >= 3)


class NestedDefaultDict(defaultdict):
    def __init__(self, depth, default=int, _root=True):
        self.root = _root
        self.depth = depth
        if depth > 1:
            cur_default = lambda: NestedDefaultDict(depth - 1,
                                                    default,
                                                    False)
        else:
            cur_default = default
        defaultdict.__init__(self, cur_default)

    def __repr__(self):
        if self.root:
            return "NestedDefaultDict(%d): {%s}" % (self.depth,
                                                    defaultdict.__repr__(self))
        else:
            return defaultdict.__repr__(self)

import collections, functools, operator

def sum_over_dict_list(dict_list):
    return dict(functools.reduce(operator.add, map(collections.Counter, dict_list)))

def combDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = {**dict1[key], **dict2[key]}

    return dict3

# filter out the zipcodes, dates and Quantity under the threshold limit
def neglect(dic, ent, thershold = 0):
    for v in dic.values():
        if ent in v.keys():
            v[ent] = v[ent] if v[ent] > thershold else 0
    return dic
# def nonEmpty(dic):
#     return list(filter(lambda x: v!=0 for v in x.values(), dic.values()))
#     return {k:v for k,v in dic.values() if not v==0}

def cleanZerovalues(d):
    clean = {}

    for k,v in d.items():
        if isinstance(v, dict):
            nested = cleanZerovalues(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif isinstance(v, float) and not v == 0:
            clean[k] = v
    return clean



# @celery.task()
def write_pii(keys, data, isUploaded):

    folder = EXAMPLES_FOLDER if not isUploaded else UPLOAD_FOLDER
    abs_file_path = Path(folder) / Path(keys).stem / "pii_json.json"

    if not abs_file_path.is_file():
        dic = makehash()
        spacy_results = makehash()
        # dic = NestedDefaultDict(2)
        parser = CommonRegex()
        nlp_model = nlp


        data = pd.read_json(data) #covert json into dataframe

        ln_data = len(list(data))
        i = iter(range(0, ln_data))

        for (colName, colData) in data.iteritems(): #list of tuples with colname and its values
            total_num = colData.shape[0]
            for key in regexes.keys():
                # breakpoint()
                if not key in ['street_addresses']:
                    dic[colName][key] = colData.astype(str).apply(lambda x: True if getattr(parser, key)(x) else False).values.sum() / total_num

                else:
                    # st.write("street address now")
                    dic[colName][key] = colData.astype(str).apply(lambda x: len(set([t[1] for t in usaddress.parse(x)])) >= 3).values.sum() / total_num
        #     my_progress_bar.progress(int((next(i)+1) / ln_data * 100))
        # my_progress_bar.empty()



        # st.write(dic)
        d = dict()

        # st.write(json.dumps(d))
        num_of_rows = 30

        for (colName, colData) in data.iloc[0:num_of_rows,:].iteritems():
            spacy_results[colName] = sum_over_dict_list(colData.astype(str).apply(lambda x: [ent.label_ for ent in nlp_model(x).ents if ent.label_ not in ['CARDINAL', 'DATE']]).tolist())
            spacy_results[colName] = {k:v / num_of_rows for k, v in spacy_results[colName].items()}

        comb_dict = combDict(dic, spacy_results)
        # st.write(comb_dict)
        comb_dict = neglect(comb_dict, 'zip_codes', 0.8)
        comb_dict = neglect(comb_dict, 'dates', 0.8)
        comb_dict = neglect(comb_dict, 'QUANTITY', 0.8)



        # script_dir = os.path.dirname(__file__)
        # rel_path = "pii_json.json"
        # abs_file_path = os.path.join(script_dir, rel_path)
        # with open(abs_file_path, 'w') as file:
        #     json.dump(comb_dict, file, sort_keys=True, indent=4)

        #write the json to a file

        with open(abs_file_path, 'w') as file:
            json.dump(comb_dict, file, sort_keys=True, indent=4)


def check_pii(keys, data, isUploaded):

    folder = EXAMPLES_FOLDER if not isUploaded else UPLOAD_FOLDER
    abs_file_path = Path(folder) / Path(keys).stem / "pii_json.json"

    # breakpoint()
    if not abs_file_path.is_file():
        # breakpoint()
        write_pii.delay(keys, data, isUploaded)

    with open(abs_file_path, 'r') as file:
        comb_dict = json.load(file)

    # st.write(comb_dict)
    # st.subheader(f"PII likelihood for {keys}")
    # st.dataframe(pd.DataFrame(cleanZerovalues(comb_dict)).fillna(0).style.highlight_max(axis=0).highlight_null())
    # st.dataframe(pd.DataFrame(cleanZerovalues(comb_dict)).style.highlight_max(axis=0).highlight_null(null_color='grey'))
    # if st.checkbox("View in JSON", key=keys):
    #     st.write(cleanZerovalues(comb_dict))
    # breakpoint()
    return pd.DataFrame(cleanZerovalues(comb_dict))





# def reporting(data):

#     st.title('Data Profiling')
#     st.subheader('Profile the above data table for the first 20 columns')

#     website_bucket_name = "piidataprofiling"
#     profile_file = "index.html"

#     if st.button('Get Data Profiling:'):
#         profiling(data=data.iloc[:, :20], website_bucket_name=website_bucket_name, profile_file=profile_file)

#         st.subheader('Data Profiling Report:')
#         url = f'https://{website_bucket_name}.s3-{REGION_NAME}.amazonaws.com/{profile_file}'
#         # if st.button('Open Data Profiling'):
#         #     webbrowser.open_new_tab(url)
#         st.write(f"open this link:{url}")

#     st.write("Compare different anonymized identities")
#     dfs = DataFrameSummary(data)
#     selected_id = st.multiselect('Select columns for summary statistics', options=data.columns.tolist()[:10],
#                                  default=data.columns.tolist()[5])
#     try:
#         idx = data.columns.tolist()[:10].index(''.join(selected_id))
#         if idx:
#             st.write(dfs[idx])
#     except ValueError:
#         logger.error(f'ERROR: Select a column to summarize')



# def Structured():

#     uploaded_file = st.file_uploader("Choose a csv file", type='csv')
#     if uploaded_file is not None:
#         # with open(uploaded_file, 'r') as file:
#         #     data = file.read().replace('\n', '')
#         data = pd.read_csv(uploaded_file, delimiter=",")
#         st.dataframe(data.head(10))
#         # st.write(type(data))

#         # uploaded = upload_to_aws(data.encode('utf8'), BUCKET_NAME, 'pii_csv.csv')
#         uploaded = upload_to_aws(data.to_csv(None).encode('utf8'), BUCKET_NAME, 'pii_csv.csv')

#         task_mode = st.selectbox("Chose the task",
#                                         ['PII Classification', 'Data Profiling'])

#         if task_mode == 'PII Classification':
#             classfication(data)
#         elif task_mode == 'Data Profiling':
#             reporting(data)




def main():

    my_text = ''
    response = ''

    # st.sidebar.title('PII Classification')
    app_mode = st.sidebar.selectbox("Chose the data type",
                                    ['Unstructured', 'Structured'])

    if app_mode == 'Unstructured':
        Unstructured()
    elif app_mode == 'Structured':
        Structured()

    # st.sidebar.info('Select the choice of demo presentation. Strucutred concerns the tabular data with PII. Anonymizing tackles the problem of sensitive info by creating a sirad id that helps maintains the integrity of the data by protecting the PII. J.S. Hastings, M. Howison, T. Lawless, J. Ucles, P. White. (2019). Unlocking Data to Improve Public Policy. Communications of the ACM 62(10): 48-53')


if __name__ == '__main__':
    # df = pd.read_csv('pii_data.csv', index_col=0)
    # a = get_pii_columns(df)
    main()
