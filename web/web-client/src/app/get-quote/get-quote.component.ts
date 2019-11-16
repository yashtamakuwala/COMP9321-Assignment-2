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
  LGAArray: Array<string> = [
    'Blacktown',
    'Botany Bay',
    'Burwood',
    'Camden',
    'Campbelltown',
    'Canada Bay',
    'Canterbury-Bankstown',
    'Cumberland',
    'Fairfield',
    'Georges River',
    'Hornsby',
    'Hunters Hill',
    'Inner West',
    'Ku-ring-gai',
    'Lane Cove',
    'Liverpool',
    'Mosman',
    'North Sydney',
    'Northern Beaches',
    'Parramatta',
    'Penrith',
    'Randwick',
    'Rockdale',
    'Ryde',
    'Strathfield',
    'Sutherland Shire',
    'Sydney',
    'The Hills Shire',
    'Waverley',
    'Willoughby',
    'Woollahra'
  ];
  propertyTypeArray: Array<string> = [
    'Apartment',
    'House',
    'Townhouse',
    'Condominium',
    'Guest suite',
    'Guesthouse',
    'Villa',
    'Serviced apartment',
    'Loft',
    'Bungalow',
    'Boutique hotel',
    'Bed and breakfast',
    'Cottage',
    'Hostel',
    'Cabin',
    'Other',
    'Hotel',
    'Tiny house',
    'Boat',
    'Camper/RV',
    'Aparthotel'
  ];
  roomTypeArray: Array<string> = [
    'Entire home/apt',
    'Private room',
    'Shared room',
    'Hotel room'
  ];
  constructor(private router: Router, private authenticationService: AuthenticationService, private webService: WebMethodsService) { }

  ngOnInit() {
    this.myform = new FormGroup({
      LGA: new FormControl(),
      propertyType: new FormControl(),
      roomType: new FormControl(),
      guestCount: new FormControl(),
      bedCount: new FormControl(),
    });
  }
  getQuote(event) {
    event.preventDefault();
    const quote = new Quote(
      this.myform.value.LGA, this.myform.value.propertyType,
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
