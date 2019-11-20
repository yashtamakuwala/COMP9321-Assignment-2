import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {WebMethodsService} from '../services/web-methods.service';
import {AuthenticationService} from '../services/authentication.service';
import {Router} from '@angular/router';
import {RatingRankingResponse} from '../models/RatingRankingResponse';

@Component({
  selector: 'app-rating-ranking',
  templateUrl: './rating-ranking.component.html',
  styleUrls: ['./rating-ranking.component.css']
})
export class RatingRankingComponent implements OnInit {

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
  responseArray = Array<RatingRankingResponse>();
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
  parseResponse(response: Array<RatingRankingResponse>) {
    this.responseArray = response;
  }
  getRatingRanking(event) {
    event.preventDefault();
    this.webservice.getRanking(this.myform.value, 'rating_ranking').subscribe(success => {
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
