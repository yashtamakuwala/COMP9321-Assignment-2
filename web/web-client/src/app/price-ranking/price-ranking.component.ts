import { Component, OnInit } from '@angular/core';
import {AuthenticationService} from '../services/authentication.service';
import {Router} from '@angular/router';
import {ReactiveFormsModule,
  FormsModule,
  FormGroup,
  FormControl,
  Validators,
  FormBuilder} from '@angular/forms';

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
  constructor(private authenticationService: AuthenticationService, private router: Router) {
    this.myform = new FormGroup({
      order: new FormControl(),
      limit: new FormControl()
    });
    this.myform.controls.order.setValue(this.orderArray[0], {onlySelf: true});
    this.myform.controls.limit.setValue(this.limitArray[0], {onlySelf: true});
  }

  ngOnInit() {
  }
  getPriceRanking(event) {
    event.preventDefault();
  }
  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
