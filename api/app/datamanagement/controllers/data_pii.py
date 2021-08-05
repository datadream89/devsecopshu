import os
from collections import defaultdict,Counter
from more_itertools import one
import functools, operator
import jsonpickle

from datamanagement.configuration import paths
from datamanagement.configuration.variables import PII_THRESHOLD
from datamanagement.controllers.data_driver import DataDriver
from datamanagement.model.feature_pii import FeaturePii
from datamanagement.model.feature_piis import FeaturePiis

from datamanagement.pii.commonregex import CommonRegex, regexes

import usaddress
import spacy
# nlp = spacy.load('en_core_web_sm')

class DataPii(DataDriver):
    def __init__(self, selected_dataset):
        DataDriver.__init__(self, selected_dataset)
        self._nlp = spacy.load('en_core_web_sm')
        self._num_of_rows = 30
        self._parser = CommonRegex()

    def load_pii_json(self):
        pii_json = self.load_json(paths.PII_SUFFIX)

        if pii_json is None:
            self.generate_pii_json()
            pii_json = self.load_json(paths.PII_SUFFIX)

        return pii_json

    def load_pii_flare_json(self):
        pii_json = self.load_json(paths.PII_FLARE_SUFFIX)

        if pii_json is None:
            self.generate_pii_json()
            pii_json = self.load_json(paths.PII_FLARE_SUFFIX)

        return pii_json

    def generate_pii_json(self):
        load_sucess = True

        if self.data is None and os.path.isfile(self.filepath):
            load_success = self.load_data()

        if load_success:
            feature_pii_collection = []
            feature_pii_collection_flare = []
            self._total_rows = self.data.shape[0]
            feature_index = 0

            for feat_name in self.data.columns.values:
                feature_pii = self.get_pii(feat_name, feature_index)
                feature_pii_collection.append(feature_pii)
                feature_pii_collection_flare.append(feature_pii.to_flare())
                feature_index += 1

            feature_piis = FeaturePiis(self.title, feature_pii_collection)
            feature_piis_json = jsonpickle.encode(feature_piis, unpicklable=False)

            self.save_json(json_to_write=feature_piis_json, suffix=paths.PII_SUFFIX)

            feature_piis_flare = FeaturePiis(self.title, feature_pii_collection_flare)
            feature_piis_flare_json = jsonpickle.encode(feature_piis_flare.to_flare(),
                                                      unpicklable=False)

            self.save_json(json_to_write=feature_piis_flare_json, suffix=paths.PII_FLARE_SUFFIX)

    def get_pii(self, feat_name, feature_index):
        var__pii_types_and_scores = self.pii_scores(feat_name)
        var__most_likely_pii_type = dict(Counter(var__pii_types_and_scores).most_common(1))
        var__is_pii = one(var__most_likely_pii_type.values()) > PII_THRESHOLD

        feature_pii = FeaturePii(feat_name=feat_name,
                                 is_pii=var__is_pii,
                                 most_likely_pii_type=var__most_likely_pii_type,
                                 pii_types_and_scores=var__pii_types_and_scores)
        return feature_pii


    def pii_scores(self, feat_name):
        pii_types_and_scores = defaultdict(lambda: "Not Present")

        colData = self.data[feat_name]
        total_num = self._total_rows
        for key in regexes.keys():
            if not key in ['street_addresses']:
                pii_types_and_scores[key] = colData.astype(str).apply(lambda x: True if getattr(self._parser, key)(x) else False).values.sum() / total_num
                pii_types_and_scores[key] = int(pii_types_and_scores[key] * 100) #convert from scores(float) to percentage(int)

            else:
                pii_types_and_scores[key] = colData.astype(str).apply(lambda x: len(set([t[1] for t in usaddress.parse(x)])) >= 3).values.sum() / total_num
                pii_types_and_scores[key] = int(pii_types_and_scores[key] * 100) #convert from scores(float) to percentage(int)


        spacy_results = defaultdict(lambda: "Not Present")
        spacy_results = sum_over_dict_list(colData.astype(str)
                                    .apply(lambda x: [ent.label_ for ent in self._nlp(x).ents
                                        if ent.label_ not in ['CARDINAL', 'DATE']]).tolist())
        spacy_results = {k:int(v * 100 / self._num_of_rows)
            for k, v in spacy_results.items()}

        comb_dict = combDict(pii_types_and_scores, spacy_results)
        # st.write(comb_dict)
        comb_dict = neglect(comb_dict, 'zip_codes', 80)
        comb_dict = neglect(comb_dict, 'dates', 80)
        comb_dict = neglect(comb_dict, 'QUANTITY', 80)

        return comb_dict


def makehash():
    return defaultdict(list)

def sum_over_dict_list(dict_list):
    return dict(functools.reduce(operator.add, map(Counter, dict_list)))

def neglect(dic, ent, thershold = 0):
    if ent in dic.keys():
        dic[ent] = dic[ent] if dic[ent] > thershold else 0
    return dic

def combDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = {**dict1[key], **dict2[key]}

    return dict3

def maxValueDict(d):
    return max(d.items(), key = lambda k: k[1])



