import { Component, OnInit } from '@angular/core';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-get-quote',
  templateUrl: './get-quote.component.html',
  styleUrls: ['./get-quote.component.css']
})
export class GetQuoteComponent implements OnInit {
  myform: FormGroup;
  constructor() { }

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

}
