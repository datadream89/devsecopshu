export class Profile {
  feat_name: string;
  feat_index: string;
  feat_datatype: string;
  feat_vartype: string;
  feat_count: string;
  feat_missing: string;
  feat_unique: string;
  feat_average: string;
  feat_median: string;
  feat_mode: string;
  feat_max: string;
  feat_min: string;
  feat_stddev: string;

  constructor(feat_name, feat_index, feat_datatype, feat_vartype, feat_count, feat_missing, feat_unique, feat_average, feat_median, feat_mode, feat_max, feat_min, feat_stddev) {
    this.feat_name = feat_name;
    this.feat_index = feat_index;
    this.feat_datatype = feat_datatype;
    this.feat_vartype = feat_vartype;
    this.feat_count = feat_count;
    this.feat_missing = feat_missing;
    this.feat_unique = feat_unique;
    this.feat_average = feat_average;
    this.feat_median = feat_median;
    this.feat_mode = feat_mode;
    this.feat_max = feat_max;
    this.feat_min = feat_min;
    this.feat_stddev = feat_stddev;
  }

}
