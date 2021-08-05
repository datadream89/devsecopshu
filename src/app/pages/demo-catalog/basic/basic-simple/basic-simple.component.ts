import { Component, OnInit } from '@angular/core';
import { RestService } from './rest.service';
import { Profile } from './Profile';
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

  headers = ["feat_name", "feat_index", "feat_datatype", "feat_vartype", "feat_count", "feat_missing", "feat_unique", "feat_average", "feat_median", "feat_mode", "feat_max", "feat_min", "feat_stddev"]

  profile: Profile[] = [];

  ngOnInit() {
    this.rs.readWeather()
      .subscribe
      (
        (response) => {
          this.profile = response[0]["data"];
        },
        (error) => {
          console.log("No Data Found" + error);
        }

      )
  }
}
