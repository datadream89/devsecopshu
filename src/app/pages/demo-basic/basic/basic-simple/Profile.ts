export class Profile {
  feat_index: any;
  feat_physical_name: any;
  feat_datatype: any;
  feat_vartype: any;
  feat_count: any;
  feat_missing: any;
  feat_unique: any;
  feat_average: any;
  feat_median: any;
  feat_max: any;
  feat_min: any;
  feat_stddev: any;
  feat_is_pii: any;
  constructor(feat_index, feat_physical_name, feat_datatype, feat_vartype, feat_count, feat_missing, feat_unique, feat_average, feat_median, feat_max, feat_min, feat_stddev, feat_is_pii) {
    
    this.feat_index = feat_index;
    this.feat_physical_name = feat_physical_name;
    this.feat_datatype = feat_datatype;
    this.feat_vartype = feat_vartype;
    this.feat_count = feat_count;
    this.feat_missing = feat_missing;
    this.feat_unique = feat_unique;
    this.feat_average = feat_average;
    this.feat_median = feat_median;
    this.feat_max = feat_max;
    this.feat_min = feat_min;
    this.feat_stddev = feat_stddev;
    this.feat_is_pii = feat_is_pii;
  }

}
