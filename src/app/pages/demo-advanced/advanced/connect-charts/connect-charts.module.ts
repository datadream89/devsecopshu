import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { ConnectChartsComponent } from './connect-charts.component';
import { RestService } from './rest.service';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    ConnectChartsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [RestService],
  bootstrap: [ConnectChartsComponent]
})
export class AppModule { }
