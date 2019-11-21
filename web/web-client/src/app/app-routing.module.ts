import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {GetQuoteComponent} from './get-quote/get-quote.component';
import {AuthGuard} from './_helpers/auth.guard';
import {PriceRankingComponent} from './price-ranking/price-ranking.component';
import {RatingRankingComponent} from './rating-ranking/rating-ranking.component';
import {UnemploymentRankingComponent} from './unemployment-ranking/unemployment-ranking.component';
import {CrimeRankingComponent} from './crime-ranking/crime-ranking.component';


const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'signup',
    component: SignupComponent
  },
  {
    path: 'properties/predictPrice',
    component: GetQuoteComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'areas/priceRank',
    component: PriceRankingComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'areas/ratingRank',
    component: RatingRankingComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'areas/unemploymentRank',
    component: UnemploymentRankingComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'areas/safetyRank',
    component: CrimeRankingComponent,
    canActivate: [AuthGuard]
  },
  {
    path: '**',
    component: LoginComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
