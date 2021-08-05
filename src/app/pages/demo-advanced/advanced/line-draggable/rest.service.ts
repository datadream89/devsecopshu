import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  private REST_API_SERVER = "http://localhost:5002/existing_rules";

  constructor(private httpClient: HttpClient) { }
  public sendGetRequest() {
    return this.httpClient.get(this.REST_API_SERVER);
  }


}
