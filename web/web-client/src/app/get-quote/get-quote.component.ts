import { Component, OnInit } from '@angular/core';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthenticationService} from '../services/authentication.service';

@Component({
  selector: 'app-get-quote',
  templateUrl: './get-quote.component.html',
  styleUrls: ['./get-quote.component.css']
})
export class GetQuoteComponent implements OnInit {
  myform: FormGroup;
  constructor(private router: Router, private authenticationService: AuthenticationService) { }

  ngOnInit() {
    this.myform = new FormGroup({
      zipCode: new FormControl(),
      propertyType: new FormControl(),
      roomType: new FormControl(),
      guestCount: new FormControl(),
      bedCount: new FormControl(),
    });
  }
  getQuote(event) {
    event.preventDefault();
    console.log(this.myform.value);
  }
  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
