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

  profileUrl: string = "http://localhost:5002/profiling";

  readWeather()
  {
    return this.http.get<Profile[]>(this.profileUrl);
  }
}
