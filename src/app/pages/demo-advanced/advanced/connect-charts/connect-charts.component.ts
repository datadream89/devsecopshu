import { Component, OnInit } from '@angular/core';
import { RestService } from './rest.service';
import { Certify} from './Certify';
declare const require: any; // DEMO IGNORE

@Component({
  selector: 'app-connect-charts',
  templateUrl: './connect-charts.component.html',
  styleUrls: ['./connect-charts.component.scss'],
})
export class ConnectChartsComponent implements OnInit {
  html = require('!!html-loader?-minimize!./connect-charts.component.html'); // DEMO IGNORE
  component = require('!!raw-loader!./connect-charts.component.ts').default; // DEMO IGNORE

  constructor(private rs: RestService) { }

  headers = ['Impacted_Key', 'Impacted_key_Value', 'column', 'message', 'row','value']

  certify: Certify[] = [];
  isShown: boolean;
  ngOnInit() {
    this.isShown = true;
    this.rs.readWeather()
      .subscribe
      (
        (response) => {
          this.isShown = !this.isShown;
          this.certify = response[0]["data"];
        },
        (error) => {
          console.log("No Data Found" + error);
        }

    )
  }
}
