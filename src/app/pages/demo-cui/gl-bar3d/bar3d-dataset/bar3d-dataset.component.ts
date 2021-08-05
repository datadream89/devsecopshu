import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
declare const require: any; // DEMO IGNORE

@Component({
  selector: 'app-bar3d-dataset',
  templateUrl: './bar3d-dataset.component.html',
  styleUrls: ['./bar3d-dataset.component.scss'],
})
export class Bar3dDatasetComponent implements OnInit {
  html = require('!!html-loader?-minimize!./bar3d-dataset.component.html'); // DEMO IGNORE
  component = require('!!raw-loader!./bar3d-dataset.component.ts').default; // DEMO IGNORE
  options: Observable<any>;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.options = this.http
      .get('assets/data/life-expectancy-table.json', { responseType: 'json' })
      .pipe(
        map((data:any[]) => ({
          grid3D: {
            },
          tooltip: {
            formatter: function (params) {

              return `${params.seriesName}<br />
              Run: ${params.data.value[0]}<br />
              Column: ${params.data.value[1]}<br />
              Exceptions: ${params.data.value[2]}
                `;
            }
          },
          xAxis3D: {
            type: 'category',
            name: '',
            axisLabel: {
              show: true,
              textStyle: {
                color: 'blue'
              }
            }
          },

          yAxis3D: {
            name:'',
            type: 'category',
            axisLabel: {
              show: true,
              textStyle: {
                color: 'red'
              }
            }


          },
          zAxis3D: [{
            name: 'Exceptions',
            nameTextStyle: {
              fontSize: 10,
              color:'gold'
            },
            axisLabel: {
              show: true,
              textStyle: {
                color: 'gold'
              }
            }
           
          }],
         
          visualMap: {
            max: 1e3
          },
          series: [
            {
              type: 'bar3D',
              data: data.map(function (item) {
                return {
                  value: [item[2], item[1], item[0]]
                }
              }),
              
              
              // symbolSize: symbolSize,
              shading: 'lambert',
            },
          ],
        })),
      );  
  }
}
