import { Component, OnInit } from '@angular/core';
import {AuthenticationService} from '../services/authentication.service';
import {Router} from '@angular/router';
import {FormControl, FormGroup} from '@angular/forms';
import {PriceRankingResponse} from '../models/PriceRankingResponse';
import {WebMethodsService} from '../services/web-methods.service';
import {CrimeRankingResponse} from '../models/CrimeRankingResponse';

@Component({
  selector: 'app-crime-ranking',
  templateUrl: './crime-ranking.component.html',
  styleUrls: ['./crime-ranking.component.css']
})
export class CrimeRankingComponent implements OnInit {
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
  responseArray = Array<CrimeRankingResponse>();
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
  parseResponse(response: Array<CrimeRankingResponse>) {
    this.responseArray = response;
  }
  getCrimeRanking(event) {
    event.preventDefault();
    this.webservice.getRanking(this.myform.value, 'crime_rankings').subscribe(success => {
      this.parseResponse(success.data);
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
