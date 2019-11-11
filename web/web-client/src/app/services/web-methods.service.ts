import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import {User} from '../models/User';
import {Observable} from 'rxjs';
import {NewUser} from '../models/NewUser';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class WebMethodsService {
  API_URL =  'http://127.0.0.1:5000/api/v1/';
  constructor(private http: HttpClient) { }

  login(user: User): Observable<any> {
    const loginUrl = this.API_URL + 'sessions';
    return this.http.post(loginUrl, user, httpOptions);
  }

  signup(user: NewUser): Observable<any> {
    const signupUrl = this.API_URL + 'users';
    return this.http.post(signupUrl, user, httpOptions);
  }
}
