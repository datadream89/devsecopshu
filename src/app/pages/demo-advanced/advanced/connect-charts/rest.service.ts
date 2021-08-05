import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Certify } from './Certify';

@Injectable({
  providedIn: 'root'
})
export class RestService implements OnInit {

  constructor(private http : HttpClient) { }

  ngOnInit(){
  }

  certifyUrl: string = "http://localhost:5002/exceptions";

  readWeather()
  {
    return this.http.get<Certify[]>(this.certifyUrl);
  }
}
