import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Profile } from './Profile';

@Injectable({
  providedIn: 'root'
})
export class RestService implements OnInit {

  constructor(private http : HttpClient) { }

  ngOnInit(){
  }

  profileUrl: string = "http://http://0.0.0.0:5002/";

  readWeather()
  {
    return this.http.get<Profile[]>(this.profileUrl);
  }
}
