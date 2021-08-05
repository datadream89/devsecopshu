from pathlib import Path
import codecs

from pandas_profiling import ProfileReport
import great_expectations as ge

from datamanagement.configuration import paths
from datamanagement.controllers.data_driver import DataDriver

class PandasProfiling(DataDriver):
  def __init__(self, selected_dataset):
    super().__init__(selected_dataset)
    self.load_data()
    self.profile_path = self.get_path_str(to_string=True)
    self.is_profiling_done = Path(self.profile_path).exists()
    self.folder_path = self.get_path_str(to_string=False).parent

  def get_path_str(self, to_string=True):
    path = Path(paths.UPLOAD_FOLDER) / self.title / paths.PROFILING_REPORT
    return str(path) if to_string else path

  def save_profiling_html(self, return_profile_html=False):
    self.load_data()
    df = self.data
    profile = ProfileReport(df, minimal=True, title="Profiling Report")
    profile.to_file(self.profile_path)
    self.is_profiling_done = True
    return profile if return_profile_html else None

  def get_profiling_html(self, as_html=False):
    if not self.is_profiling_done:
      self.save_profiling_html(as_html)
    return self.profile_path if not as_html else codecs.open(self.profile_path, "rb").read()

  def get_data_context_setup(func):
    def wrapper(*args):
      import subprocess
      subprocess.Popen("great_expectations init", shell=True, cwd=args[0].folder_path)
      return func(*args)
    return wrapper

  @get_data_context_setup
  def get_expectation_suite(self, profile):
    data_context = ge.DataContext(context_root_dir=str(self.folder_path))
    suite = profile.to_expectation_suite(
      suite_name=f"{self.title}_expectations",
      data_context=data_context,
      save_suite=False,
      run_validation=False,
      build_data_docs=False)
    data_context.save_expectation_suite(suite)
    return suite, data_context

  def run_validation(self, suite, data_context):
    batch = ge.dataset.PandasDataset(self.data, expectation_suite=suite)
    results = data_context.run_validation_operator(
      "action_list_operator", assets_to_validate=[batch]
    )
    validation_result_identifier = results.list_validation_result_identifiers()[0]
    #https://github.com/pandas-profiling/pandas-profiling/blob/develop/examples/features/great_expectations_example.py
    data_context.build_data_docs()
    data_context.open_data_docs(validation_result_identifier)


