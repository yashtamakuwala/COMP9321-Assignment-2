import { Component, OnInit } from '@angular/core';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthenticationService} from '../services/authentication.service';
import {Quote} from '../models/Quote';
import {WebMethodsService} from '../services/web-methods.service';

@Component({
  selector: 'app-get-quote',
  templateUrl: './get-quote.component.html',
  styleUrls: ['./get-quote.component.css']
})
export class GetQuoteComponent implements OnInit {
  myform: FormGroup;
  constructor(private router: Router, private authenticationService: AuthenticationService, private webService: WebMethodsService) { }

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
    const quote = new Quote(
      this.myform.value.zipCode, this.myform.value.propertyType,
      this.myform.value.roomType, this.myform.value.guestCount,
      this.myform.value.bedCount);
    this.webService.getQuote(quote).subscribe(success => {
      console.log(success);
    }, error => {
      console.log(error);
    });
  }
  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
