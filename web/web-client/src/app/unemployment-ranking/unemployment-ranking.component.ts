import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {PriceRankingResponse} from '../models/PriceRankingResponse';
import {WebMethodsService} from '../services/web-methods.service';
import {AuthenticationService} from '../services/authentication.service';
import {Router} from '@angular/router';
import {UnemploymentRankingResponse} from '../models/UnemploymentRankingResponse';

@Component({
  selector: 'app-unemployment-ranking',
  templateUrl: './unemployment-ranking.component.html',
  styleUrls: ['./unemployment-ranking.component.css']
})
export class UnemploymentRankingComponent implements OnInit {

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
  responseArray = Array<UnemploymentRankingResponse>();
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
  parseResponse(response: Array<UnemploymentRankingResponse>) {
    this.responseArray = response;
  }
  getUnemploymentRanking(event) {
    event.preventDefault();
    this.webservice.getRanking(this.myform.value, 'unemployment_rankings').subscribe(success => {
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
