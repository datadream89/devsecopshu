import { Component, OnInit } from '@angular/core';
import { RestService } from './rest.service';
import { Profile } from './Profile';
//import { SpinnerVisibilityService } from 'ng-http-loader'
declare const require: any; // DEMO IGNORE

@Component({
  selector: 'app-basic-simple',
  templateUrl: './basic-simple.component.html',
  styleUrls: ['./basic-simple.component.scss'],
})
export class BasicSimpleComponent implements OnInit {
  html = require('!!html-loader?-minimize!./basic-simple.component.html'); // DEMO IGNORE
  component = require('!!raw-loader!./basic-simple.component.ts').default; // DEMO IGNORE

  constructor(private rs: RestService) { }

  headers = ["feat_index","feat_physical_name",  "feat_datatype", "feat_vartype", "feat_count", "feat_missing", "feat_unique", "feat_average", "feat_median", "feat_max", "feat_min", "feat_stddev", "feat_is_pii"]

  profile: Profile[] = [];
  isShown: boolean;
  ngOnInit() {
    this.isShown = true;
    this.rs.readWeather()
      .subscribe
      (
        (response) => {
          this.isShown = !this.isShown;
          this.profile = response[0]["data"];
        },
        (error) => {
          console.log("No Data Found" + error);
        }

    )
  }
}
