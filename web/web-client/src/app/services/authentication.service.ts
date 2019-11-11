import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {AuthenticatedUser} from '../models/AuthenticatedUser';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private currentUser: AuthenticatedUser;
  constructor() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
  }
  public get currentUserValue(): AuthenticatedUser {
    return this.currentUser;
  }
  login(authenticatedUser: AuthenticatedUser) {
    sessionStorage.setItem('currentUser', JSON.stringify(authenticatedUser));
  }
  logout() {
    sessionStorage.removeItem('currentUser');
  }
}
