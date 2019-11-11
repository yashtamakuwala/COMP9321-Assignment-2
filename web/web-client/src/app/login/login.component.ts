import { Component, OnInit } from '@angular/core';
import {WebMethodsService} from '../services/web-methods.service';
import {User} from '../models/User';
import { Router } from '@angular/router';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';
import {AuthenticatedUser} from '../models/AuthenticatedUser';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  myform: FormGroup;
  user: User;
  error: boolean;
  constructor(private webService: WebMethodsService, private router: Router) { }

  ngOnInit() {
    this.myform = new FormGroup({
      email: new FormControl(),
      password: new FormControl()
    });
    this.user = new User();
    this.error = false;
  };
  onLogIn(event) {
    event.preventDefault();
    this.user.email = this.myform.value.email;
    this.user.password = this.myform.value.password;
    this.webService.login(this.user).subscribe(success => {
      const authUser = new AuthenticatedUser(success.email, success.is_admin, success.token);
      console.log(authUser);
      // extract api key and save it to session storage
      this.router.navigate(['/quote']);
    }, error => {
      this.error = true;
    });
  }
}
