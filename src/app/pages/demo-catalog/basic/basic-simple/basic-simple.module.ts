import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { BasicSimpleComponent } from './basic-simple.component';
import { RestService } from './rest.service';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    BasicSimpleComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [RestService],
  bootstrap: [BasicSimpleComponent]
})
export class AppModule { }
