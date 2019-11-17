import { Component, OnInit } from '@angular/core';
import {AuthenticationService} from '../services/authentication.service';
import {Router} from '@angular/router';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';
import {WebMethodsService} from '../services/web-methods.service';
import {PriceRankingResponse} from '../models/PriceRankingResponse';

@Component({
  selector: 'app-price-ranking',
  templateUrl: './price-ranking.component.html',
  styleUrls: ['./price-ranking.component.css']
})
export class PriceRankingComponent implements OnInit {
  myform: FormGroup;
  orderArray: Array<string> = [
    'ascending',
    'descending',
  ];
  limitArray: Array<string> = [
    '5',
    '10',
    '20',
    'all'
  ];
  responseArray = Array<PriceRankingResponse>();
  constructor(private webservice: WebMethodsService, private authenticationService: AuthenticationService, private router: Router) {
    this.myform = new FormGroup({
      order: new FormControl(),
      limit: new FormControl()
    });
    this.myform.controls.order.setValue(this.orderArray[0], {onlySelf: true});
    this.myform.controls.limit.setValue(this.limitArray[0], {onlySelf: true});
  }

  ngOnInit() {
  }
  parseResponse(response: Array<PriceRankingResponse>) {
    this.responseArray = response;
  }
  getPriceRanking(event) {
    event.preventDefault();
    this.webservice.getPriceRanking(this.myform.value, 'price_rankings').subscribe(success => {
      this.parseResponse(success.data);
    }, error => {
      console.log(error);
    });
  }
  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
