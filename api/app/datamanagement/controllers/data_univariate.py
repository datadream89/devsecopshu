import os
import jsonpickle
import seaborn as sns

from datamanagement.configuration import const_types
from datamanagement.configuration import paths
from datamanagement.controllers.data_driver import DataDriver
from datamanagement.controllers.data_pii import DataPii
from datamanagement.model.feature import Feature
from datamanagement.model.features import Features

from collections import defaultdict
import pandas as pd
import numpy as np


class DataUnivariate(DataDriver):
    def __init__(self, selected_dataset):
        DataDriver.__init__(self, selected_dataset)
        self.pii_data = DataPii(selected_dataset).load_pii_json()

    def load_features_json(self):
        features_json = self.load_json(paths.FEATURES_SUFFIX)

        # If the file doesn't exist, generate it
        if features_json is None:
            self.generate_features_json()
            features_json = self.load_json(paths.FEATURES_SUFFIX)

        # Return the JSON
        return features_json

    def generate_features_json(self):
        load_success = True

        # Check if the data file exists, and if so, load the data as needed
        if self.data is None and os.path.isfile(self.filepath):
            load_success = self.load_data()

        if load_success:
            features_collection = []
            feature_index = 0

            for feat_physical_name in self.data.columns.values:
                feature = self.get_feature(feat_physical_name, feature_index)
                features_collection.append(feature)
                feature_index += 1

            # Create object holding features collection and save as JSON
            features = Features(self.title, features_collection)
            features_json = jsonpickle.encode(features, unpicklable=False,)

            # Save the serialized JSON to a file
            self.save_json(json_to_write=features_json, suffix=paths.FEATURES_SUFFIX)

    def get_feature(self, feat_physical_name, feature_index):
        var_datatype = self.get_data_type(feat_physical_name)
        var_vartype = self.get_vartype_formatted(feat_physical_name)
        var_count = self.get_count(feat_physical_name)
        var_missing = self.get_missing_formatted(feat_physical_name)
        var_unique = self.get_count_unique(feat_physical_name)

        # Numeric only
        var_avg = self.format_rounded_string(self.get_average(feat_physical_name))
        var_median = self.get_median(feat_physical_name)
        var_mode = self.get_mode(feat_physical_name)
        var_max = self.get_max(feat_physical_name)
        var_min = self.get_min(feat_physical_name)
        var_stddev = self.format_rounded_string(self.get_stddev(feat_physical_name))
        var_variance = self.format_rounded_string(self.get_variance(feat_physical_name))
        var_quantile25 = self.format_rounded_string(self.get_quantile25(feat_physical_name))
        var_quantile75 = self.format_rounded_string(self.get_quantile75(feat_physical_name))
        var_iqr = self.format_rounded_string(self.get_iqr(feat_physical_name))
        var_skew = self.format_rounded_string(self.get_skew(feat_physical_name))
        var_kurtosis = self.format_rounded_string(self.get_kurtosis(feat_physical_name))
        var_outlier_score = self.get_outlier_score(feat_physical_name)

        # Non-numeric only
        var_mostcommon = self.get_mostcommon(feat_physical_name)
        var_5_mostcommon_values, var_5_mostcommon_counts = self.get_n_mostcommon(feat_physical_name, 5)
        var_leastcommon = self.get_leastcommon(feat_physical_name)
        var_5_leastcommon_values, var_5_leastcommon_counts = self.get_n_leastcommon(feat_physical_name, 5)
        var_max_length = self.get_max_length(feat_physical_name)
        var_min_length = self.get_min_length(feat_physical_name)



        # Graphs
        # graph_histogram = self.get_histogram(feat_physical_name)
        # graph_countplot = self.get_countplot(feat_physical_name)

        # Errors, warnings, and info
        feat_errors = self.get_errors(feat_physical_name)
        feat_warnings = self.get_warnings(feat_physical_name)
        feat_notes = self.get_notes(feat_physical_name)

        # Pii information
        var__is_pii = self.pii_data['piis'][feature_index]['is_pii']
        var__pii_type = self.pii_data['piis'][feature_index]['most_likely_pii_type']

        # Save the feature stats
        feature = Feature(feat_physical_name=feat_physical_name,
                          feat_index=feature_index,
                          feat_datatype=var_datatype,
                          feat_vartype=var_vartype,
                          feat_count=var_count,
                          feat_missing=var_missing,
                          feat_unique=var_unique,
                          feat_average=var_avg,
                          feat_median=var_median,
                          feat_mode=var_mode,
                          feat_max=var_max,
                          feat_max_length=var_max_length,
                          feat_min=var_min,
                          feat_min_length=var_min_length,
                          feat_stddev=var_stddev,
                          feat_variance=var_variance,
                          feat_quantile25=var_quantile25,
                          feat_quantile75=var_quantile75,
                          feat_iqr=var_iqr,
                          feat_skew=var_skew,
                          feat_kurtosis=var_kurtosis,
                          feat_mostcommon=var_mostcommon,
                          feat_5_mostcommon_values=var_5_mostcommon_values,
                          feat_5_mostcommon_counts=var_5_mostcommon_counts,
                          feat_leastcommon=var_leastcommon,
                          feat_5_leastcommon_values=var_5_leastcommon_values,
                          feat_5_leastcommon_counts=var_5_leastcommon_counts,
                        #   graph_histogram=graph_histogram,
                        #   graph_countplot=graph_countplot,
                          feat_errors=feat_errors,
                          feat_warnings=feat_warnings,
                          feat_notes=feat_notes,
                          feat_outlierscore=var_outlier_score,
                          feat_is_pii=var__is_pii,
                          feat_pii_type=var__pii_type)
        return feature

    def get_count(self, feat_physical_name):
        return int(self.data[feat_physical_name].count())

    def get_count_missing(self, feat_physical_name):
        return int(self.data[feat_physical_name].isnull().sum())

    def get_percent_missing(self, feat_physical_name):
        missing_count = self.get_count_missing(feat_physical_name)
        missing_percent = 100 * missing_count / float(self.data.shape[0])
        return missing_percent

    def get_missing_formatted(self, feat_physical_name):
        return str("%s (%.3f%%)" % (self.get_count_missing(feat_physical_name), self.get_percent_missing(feat_physical_name)))

    def get_vartype_formatted(self, feat_physical_name):
        vartype = self.get_variable_type(feat_physical_name)

        # Denote label and index, if applicable
        if self.id_column is not None and feat_physical_name == self.id_column:
            vartype += " (ID)"
        elif self.label_column is not None and feat_physical_name == self.label_column:
            vartype += " (Label)"

        return vartype

    # def feat_is_numeric(self, feat_physical_name):
    #     return self.data[feat_physical_name].dtype in ['int64', 'float64']

    def feat_is_numeric(self, feat_physical_name):
        # self.data[feat_physical_name] = self.data[feat_physical_name].astype(self.get_data_type(feat_physical_name))
        return self.get_data_type(feat_physical_name) in ['Integer', 'Float']

    def get_average(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return float(self.data[feat_physical_name].mean())
        return None

    def get_median(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return float(self.data[feat_physical_name].median())
        return None

    def get_mode(self, feat_physical_name):
        var_mode = ""
        mode = self.data[feat_physical_name].mode()

        if mode is not None:
            for m in mode:
                var_mode = var_mode + str(m) + " "

        # If no mode is found, return None instead of empty string
        if var_mode == "":
            var_mode = None

        return var_mode

    def get_max(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return float(self.data[feat_physical_name].max())
        return None

    def get_max_length(self, feat_physical_name):
        try:
            if not self.feat_is_numeric(feat_physical_name):
                return len(max(self.data[feat_physical_name], key=len))
        except:
            return None

    def get_min(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return float(self.data[feat_physical_name].min())
        return None

    def get_min_length(self, feat_physical_name):
        try:
            if not self.feat_is_numeric(feat_physical_name):
                return len(min(self.data[feat_physical_name], key=len))
        except:
            return None

    def get_stddev(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].std()
        return None

    def get_variance(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].var()
        return None

    def get_quantile25(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].dropna().quantile(q=0.25)
        return None

    def get_quantile75(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].dropna().quantile(q=0.75)
        return None

    def get_iqr(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.get_quantile75(feat_physical_name) - self.get_quantile25(feat_physical_name)
        return None

    def get_outlier_score(self, feat_physical_name):
        lower_bound = self.get_quantile25(feat_physical_name)
        upper_bound = self.get_quantile75(feat_physical_name)
        return sum(self.data[feat_physical_name].dropna().between(lower_bound, upper_bound))



    def get_skew(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].skew()
        return None

    def get_kurtosis(self, feat_physical_name):
        if self.feat_is_numeric(feat_physical_name):
            return self.data[feat_physical_name].kurt()
        return None

    def get_mostcommon(self, feat_physical_name):
        if not self.feat_is_numeric(feat_physical_name):
            return str("%s (%d)" % (self.data[feat_physical_name].value_counts().idxmax(),
                                    self.data[feat_physical_name].value_counts().max()))
        return None

    def get_n_mostcommon(self, feat_physical_name, n):
        if not self.feat_is_numeric(feat_physical_name):
            df = self.data[feat_physical_name].value_counts()[:n].rename_axis(f'Top {n} Most Common').reset_index(name='Counts')
            # breakpoint()
            return list(df[f'Top {n} Most Common']), list(list(df['Counts'].map(str)))
        return None, None


    def get_leastcommon(self, feat_physical_name):
        if not self.feat_is_numeric(feat_physical_name):
            return str("%s (%d)" % (self.data[feat_physical_name].value_counts().idxmin(),
                                    self.data[feat_physical_name].value_counts().min()))
        return None

    def get_n_leastcommon(self, feat_physical_name, n):
        if not self.feat_is_numeric(feat_physical_name):
            df = self.data[feat_physical_name].value_counts()[-n:].rename_axis(f'Top {n} Least Common').reset_index(name='Counts')
            # breakpoint()
            return list(df[f'Top {n} Least Common']), list(df['Counts'].map(str))
        return None, None

    def get_histogram(self, feat_physical_name):
        if self.get_data_type(feat_physical_name) in [const_types.DATATYPE_FLOAT, const_types.DATATYPE_INTEGER]:
            hist_plot = sns.distplot(self.data[feat_physical_name].dropna(), bins=None, hist=True, kde=False, rug=False)
            return self.save_graph(hist_plot, feat_physical_name + paths.FILE_HISTOGRAM)
        return None

    def get_countplot(self, feat_physical_name):
        if self.get_data_type(feat_physical_name) not in [const_types.DATATYPE_FLOAT, const_types.DATATYPE_INTEGER] and \
           self.check_uniques_for_graphing(feat_physical_name):
                countplot = sns.countplot(y=self.data[feat_physical_name].dropna())
                return self.save_graph(countplot, filename=feat_physical_name + paths.FILE_COUNTPLOT)
        return None

    def get_errors(self, feat_physical_name):
        return None

    def get_warnings(self, feat_physical_name):
        warnings = []
        if self.get_percent_unique(feat_physical_name) == 1:
            warnings.append("This feature has all unique values")
        if self.get_percent_missing(feat_physical_name) >= 50:
            warnings.append("This feature is missing in 50% or more rows")
        return warnings

    def get_notes(self, feat_physical_name):
        notes = []
        if self.get_percent_missing(feat_physical_name) == 0:
            notes.append("This feature is not missing any values")
        return notes


    @staticmethod
    def make_dict():
        return defaultdict(make_dict)

    @staticmethod
    def get_nested_list(values, counts, total_size, name, feat_name):
        # list_values = [values, counts, np.array(counts)/np.float64(total_size)]
        list_values = [values, counts, np.array(list(map(int, counts)))/pd.to_numeric(total_size)] #if values is None else [None, None, None]
        list_keys = ['values', 'counts', 'score']
        dict_items = dict(zip(list_keys, list_values))
        return pd.concat({name: pd.DataFrame(dict_items)}, axis=1)

    def frequency_stats(self):
        if not self.file_exists(paths.FREQUENCY_CSV_SUFFIX):
            self.generate_frequency_csv()
        return self.load_data()

    def load_frequency_json(self):
        frequency_json = self.load_json(paths.FREQUENCY_SUFFIX)

        # If the file doesn't exist, generate it
        if frequency_json is None:
            self.generate_frequencies_json()
            frequency_json = self.load_json(paths.FREQUENCY_SUFFIX)

        # Return the JSON
        return frequency_json

    @staticmethod
    def nest(d: dict) -> dict:
      result = {}
      for key, value in d.items():
          target = result
          for k in key[:-1]:  # traverse all keys but the last
              target = target.setdefault(k, {})
          target[key[-1]] = value
      return result

    @staticmethod
    def df_to_nested_dict(df: pd.DataFrame) -> dict:
      d = df.to_dict(orient='index')
      return {k: DataUnivariate.nest(v) for k, v in d.items()}

    def generate_frequencies_json(self):
      features = self.load_features_json()
      d = pd.DataFrame() #default_dict(make_dict)
      for f in features["features"]:
        if f["feat_5_mostcommon_values"] and f["feat_5_leastcommon_values"]:
          df1 = DataUnivariate.get_nested_list(f["feat_5_mostcommon_values"], f["feat_5_mostcommon_counts"], f["feat_count"], name="Most_Common", feat_name=f["feat_physical_name"])
          df2 = DataUnivariate.get_nested_list(f["feat_5_leastcommon_values"], f["feat_5_leastcommon_counts"], f["feat_count"], name="Least_Common", feat_name=f["feat_physical_name"])
          df_1_2 = pd.concat([df1, df2], axis=1)
          df_1_2['feat_physical_name'] = f["feat_physical_name"]
          d = pd.concat([d, df_1_2], axis=0)
          d.reset_index(drop=True, inplace=True)

      # frequency_json = jsonpickle.encode(d.to_json(orient = "split"))
      frequency_nested_dict = DataUnivariate.df_to_nested_dict(d)
      frequency_json = jsonpickle.encode(frequency_nested_dict)
      # Save the serialized JSON to a file
      self.save_json(json_to_write=frequency_json, suffix=paths.FREQUENCY_SUFFIX)
        # d.to_pickle("./frequency.pkl")
        # self.save_csv(d, paths.FREQUENCY_CSV_SUFFIX)
