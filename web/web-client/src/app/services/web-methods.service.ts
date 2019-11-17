import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import {User} from '../models/User';
import {Observable} from 'rxjs';
import {NewUser} from '../models/NewUser';
import {Quote} from '../models/Quote';
import {AuthenticationService} from './authentication.service';
import {PriceRanking} from '../models/PriceRanking';

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
  constructor(private http: HttpClient, private authenticationService: AuthenticationService) { }

  login(user: User): Observable<any> {
    const loginUrl = this.API_URL + 'sessions';
    return this.http.post(loginUrl, user, httpOptions);
  }

  signup(user: NewUser): Observable<any> {
    const signupUrl = this.API_URL + 'users';
    return this.http.post(signupUrl, user, httpOptions);
  }

  getQuote(quote: Quote): Observable<any> {
    const quoteUrl = this.API_URL + 'predictions';
    let headers_ = new HttpHeaders();
    headers_ = headers_.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const params_ = new HttpParams()
      .set('lga', String(quote.lga))
      .set('property_type', quote.property_type)
      .set('room_type', quote.room_type)
      .set('guest_count', String(quote.guest_count))
      .set('bed_count', String(quote.bed_count));
    return this.http.get(quoteUrl, {params: params_, headers: headers_});
  }
  getRanking(priceRanking: PriceRanking, functionName: string): Observable<any> {
    const queryUrl = this.API_URL + functionName;
    let headers_ = new HttpHeaders();
    headers_ = headers_.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const params_ = new HttpParams()
      .set('order', priceRanking.order)
      .set('limit', priceRanking.limit);
    return this.http.get(queryUrl, {params: params_, headers: headers_});
  }

}
