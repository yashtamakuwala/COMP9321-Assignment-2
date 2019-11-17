import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SignupComponent } from './signup/signup.component';
import { GetQuoteComponent } from './get-quote/get-quote.component';
import { LoginComponent } from './login/login.component';
import {ReactiveFormsModule} from '@angular/forms';
import { PriceRankingComponent } from './price-ranking/price-ranking.component';
import { RatingRankingComponent } from './rating-ranking/rating-ranking.component';
import { CrimeRankingComponent } from './crime-ranking/crime-ranking.component';
import { UnemploymentRankingComponent } from './unemployment-ranking/unemployment-ranking.component';


@NgModule({
  declarations: [
    AppComponent,
    SignupComponent,
    GetQuoteComponent,
    LoginComponent,
    PriceRankingComponent,
    RatingRankingComponent,
    CrimeRankingComponent,
    UnemploymentRankingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
