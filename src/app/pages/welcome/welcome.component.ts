import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { DataService } from './data.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup } from "@angular/forms";
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss'],
})
export class WelcomeComponent {

  url: string = "http://ec2-18-212-179-177.compute-1.amazonaws.com:4200/";
  urlSafe: SafeResourceUrl;
  constructor(private dataService: DataService, private httpClient: HttpClient, public fb: FormBuilder, public sanitizer: DomSanitizer) {

  }



  ngOnInit() {
    this.urlSafe = this.sanitizer.bypassSecurityTrustResourceUrl(this.url);
  }
}
