import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
declare const require: any; // DEMO IGNORE

@Component({
  selector: 'app-gl-bar3d',
  templateUrl: './gl-bar3d.component.html',
  styleUrls: ['./gl-bar3d.component.scss'],
})

export class GlBar3dComponent {
  html = require('!!html-loader?-minimize!./gl-bar3d.component.html'); // DEMO IGNORE
  component = require('!!raw-loader!./gl-bar3d.component.ts').default; // DEMO IGNORE
  name = 'Set iframe source';
  url: string = "http://http://0.0.0.0:5002/unstructured";
  urlSafe: SafeResourceUrl;
  urlIn: string = "http://http://0.0.0.0:5002/unstructured_text";
  urlInSafe: SafeResourceUrl;
  theme: string;
  options = {
    title: {
      text: 'Nightingale\'s Rose Diagram',
      subtext: 'Mocking Data',
      x: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
      x: 'center',
      y: 'bottom',
      data: ['rose1', 'rose2', 'rose3', 'rose4', 'rose5', 'rose6', 'rose7', 'rose8']
    },
    calculable: true,
    series: [
      {
        name: 'area',
        type: 'pie',
        radius: [30, 110],
        roseType: 'area',
        data: [
          { value: 10, name: 'rose1' },
          { value: 5, name: 'rose2' },
          { value: 15, name: 'rose3' },
          { value: 25, name: 'rose4' },
          { value: 20, name: 'rose5' },
          { value: 35, name: 'rose6' },
          { value: 30, name: 'rose7' },
          { value: 40, name: 'rose8' }
        ]
      }
    ]
  };

  constructor(public sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.urlInSafe = this.sanitizer.bypassSecurityTrustResourceUrl(this.urlIn);
    this.urlSafe = this.sanitizer.bypassSecurityTrustResourceUrl(this.url);
  }
}

