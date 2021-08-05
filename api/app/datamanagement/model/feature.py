from typing import Optional
from xxlimited import Null


# class Feature(object):
#     def __init__(self, feat_physical_name, feat_index, feat_datatype="", feat_vartype="", feat_count="",
#                  feat_missing="", feat_unique="", feat_average="", feat_median="", feat_mode="",
#                  feat_max="", feat_max_length="", feat_min="", feat_min_length="", feat_stddev="", feat_variance="", feat_skew="",
#                  feat_kurtosis="",feat_quantile25="", feat_quantile75="", feat_iqr="", feat_mostcommon="", feat_5_mostcommon_values="",
#                  feat_5_mostcommon_counts="", feat_leastcommon="", feat_5_leastcommon_values="", feat_5_leastcommon_counts="",
#                  graph_histogram: Optional[str]="", graph_countplot: Optional[str]="", feat_errors="",
#                  feat_warnings="", feat_notes="", feat_outlierscore=""):
#         # Feature stats
#         self.feat_physical_name = feat_physical_name
#         self.feat_index = feat_index
#         self.feat_datatype = feat_datatype
#         self.feat_vartype = feat_vartype
#         self.feat_count = feat_count
#         self.feat_missing = feat_missing
#         self.feat_unique = feat_unique

#         # Numeric only
#         self.feat_average = feat_average
#         self.feat_median = feat_median
#         self.feat_mode = feat_mode
#         self.feat_max = feat_max
#         self.feat_min = feat_min
#         self.feat_stddev = feat_stddev
#         self.feat_variance = feat_variance
#         self.feat_skew = feat_skew
#         self.feat_kurtosis = feat_kurtosis
#         self.feat_quantile_25 = feat_quantile25
#         self.feat_quantile_75 = feat_quantile75
#         self.feat_iqr = feat_iqr
#         self.feat_outlierscore=feat_outlierscore

#         # Categorical only
#         self.feat_mostcommon = feat_mostcommon
#         self.feat_5_mostcommon_values = feat_5_mostcommon_values
#         self.feat_5_mostcommon_counts = feat_5_mostcommon_counts
#         self.feat_leastcommon = feat_leastcommon
#         self.feat_5_leastcommon_values = feat_5_leastcommon_values
#         self.feat_5_leastcommon_counts = feat_5_leastcommon_counts
#         self.feat_max_length = feat_max_length
#         self.feat_min_length = feat_min_length

#         # Visualizations
#         self.graph_histogram = graph_histogram
#         self.graph_countplot = graph_countplot

#         # Warnings, errors, and notes
#         self.errors = feat_errors
#         self.warnings = feat_warnings
#         self.notes = feat_notes

class Feature(object):
  def __init__(self, feat_physical_name, feat_index, **kwargs):
    self.feat_physical_name = feat_physical_name
    self.feat_index = feat_index
    for attr, val in kwargs.items():
      setattr(self, attr, (lambda x: '' if x is None else x)(val))
