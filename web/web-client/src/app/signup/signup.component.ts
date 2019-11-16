import { Component, OnInit } from '@angular/core';
import { NewUser } from '../models/NewUser';
import {WebMethodsService} from '../services/web-methods.service';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';
import {isBoolean} from 'util';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  myform: FormGroup;
  newUser: NewUser;
  error: string;
  hasError: boolean;
  signUpUnsuccessful: boolean;
  responseReceived: boolean;
  constructor(private webService: WebMethodsService) { }

  ngOnInit() {
    this.myform = new FormGroup({
      email: new FormControl('', [
        Validators.email,
        Validators.required
      ]),
      password: new FormControl('', [
        Validators.required
      ]),
      confirmPassword: new FormControl('', [
        Validators.required
      ]),
      firstName: new FormControl('', [
        Validators.required
      ]),
      lastName: new FormControl('', [
        Validators.required
      ])
    });
    this.newUser = new NewUser();
    this.error = 'The passwords do not match';
    this.hasError = false;
    this.responseReceived = false;
    this.signUpUnsuccessful = false;
  }
  onSignUp(event) {
    event.preventDefault();
    this.newUser.email = this.myform.value.email;
    const confirmPassword = this.myform.value.confirmPassword;
    this.newUser.password = this.myform.value.password;
    this.newUser.first_name = this.myform.value.firstName;
    this.newUser.last_name = this.myform.value.lastName;
    if (confirmPassword === this.newUser.password) {
      this.hasError = false;
      this.webService.signup(this.newUser).subscribe(x => {
        this.responseReceived = true;
        this.signUpUnsuccessful = false;
      },
        msg => {
          this.signUpUnsuccessful = true;
        });
    } else {
      this.hasError = true;
    }
  }


}
