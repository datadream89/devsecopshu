import os

UPLOAD_RELATIVE = 'static/uploads/'
EXAMPLES_RELATIVE = 'static/data/'
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_RELATIVE)
EXAMPLES_FOLDER = os.path.join(APP_ROOT, EXAMPLES_RELATIVE)
GRAPHS_SUBFOLDER = "/graphs/"

DATASETS = os.path.join(EXAMPLES_FOLDER, "datasets.csv")
DATASETS_JSON = os.path.join(EXAMPLES_FOLDER, "datasets.json")

# Graph types
FILE_BARCHART = "_bar.png"
FILE_BOXCHART = "_box.png"
FILE_SCATTERPLOT = "_scatter.png"
FILE_COUNTPLOT = "_countplot.png"
FILE_HISTOGRAM = "_hist.png"

# File endings
SUMMARY_SUFFIX = "summary.json"
FEATURES_SUFFIX = "features.json"
INTERACTIONS_SUFFIX = "interactions.json"
PII_SUFFIX = "pii.json"
PII_FLARE_SUFFIX = "pii_flare.json"
ERRORS_SUFFIX = "errors.json"
FREQUENCY_SUFFIX = "frequency_stats.json"

PROFILING_REPORT = "profiling_report.html"

FREQUENCY_CSV_SUFFIX = "frequency_stats.csv"
FEATURES_CSV_SUFFIX = "features.csv"
PII_CSV_SUFFIX = "pii.csv"
SUMMARY_CSV_SUFFIX = "summary.csv"

#Exceptions
PII_EXCEPTIONS = "pii_exceptions.txt"

#DataFrame pickle names
FREQUENCY_DF = "frequency_df"
